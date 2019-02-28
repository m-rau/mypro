from core4.api.v1.application import CoreApiContainer
from core4.api.v1.server import CoreApiServer
from mypro.api.prime import PrimeHandler


class PrimeServer(CoreApiContainer):
    rules = [
        (r'/prime', PrimeHandler)
    ]


if __name__ == '__main__':
    from core4.api.v1.tool.functool import serve
    serve(PrimeServer, CoreApiServer)
