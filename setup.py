from setuptools import find_packages

try:
    from core4.setup import setup
except:
    from core4.script.installer.core4.setup import setup

import mypro



setup(
    name="mypro",
    version=mypro.__version__,
    packages=find_packages(exclude=['docs*', 'tests*'])
)
