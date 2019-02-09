from core4.api.v1.request.main import CoreRequestHandler
from core4.api.v1.application import CoreApiContainer


class TestHandler(CoreRequestHandler):

    author = "mra"
    title = "test handler"

    def get(self):
        self.reply("hello world")



class TestServer(CoreApiContainer):
    root = "/test-server"
    rules = [
        (r'/test', TestHandler)
    ]


if __name__ == '__main__':
    from core4.api.v1.tool.functool import serve
    serve(TestServer)