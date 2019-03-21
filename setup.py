import json
import os
import sys
from subprocess import check_call

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

import mypro

if sys.version_info < (3, 5):
    sys.exit('requires Python 3.5 or higher')

# ensure pip >= 18.1
import pip

if tuple([int(i) for i in pip.__version__.split(".")]) < (18, 1):
    sys.exit("requires pip version 18.1 or higher, "
             "Upgrade with `pip install --upgrade pip`")


def read_install_requires():
    source = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          "install_requires.txt"))
    if os.path.exists(source):
        with open(source, "r", encoding="utf-8") as fh:
            return [pkg.strip() for pkg in fh.readlines()]
    return []


class BuildCore4(build_py):
    def run(self):
        build = []
        start_dir = os.path.abspath(os.curdir)
        if "" not in self.package_data:
            self.package_data[""] = []
        for package in self.packages:
            package_dir = os.path.abspath(self.get_package_dir(package))
            os.chdir(package_dir)
            self.package_data[""].append(package + ".yaml")
            for (path, directories, filenames) in os.walk("."):
                for filename in filenames:
                    if filename == "package.json":
                        with open(os.path.join(path, filename), 'r',
                                  encoding="utf-8") as fh:
                            package_json = json.load(fh)
                        if "core4" in package_json:
                            print("installing webapps", package_dir + ":",
                                  path)
                            command = package_json["core4"].get(
                                "build_command", [])
                            dist = package_json["core4"].get("dist", None)
                            if dist:
                                build.append((path, dist, command))
            for path, dist, command in build:
                os.chdir(path)
                for part in command:
                    check_call(part, shell=True)
                for (root, directories, filenames) in os.walk(dist):
                    for filename in filenames:
                        full_path = os.path.join(path, root, filename)
                        self.package_data[""].append(full_path)
                os.chdir(package_dir)
            os.chdir(start_dir)
        build_py.run(self)


setup(
    name="mypro",
    version=mypro.__version__,
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=read_install_requires() + [
        # put your package requirements here or into install_requires.txt
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        "Operating System :: POSIX :: Linux"
    ],
    zip_safe=False,
    cmdclass={
        'build_py': BuildCore4,
    },
)
