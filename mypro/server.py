from core4.api.v1.request.main import CoreRequestHandler
from core4.api.v1.application import CoreApiContainer
from core4.queue.helper.functool import enqueue


class PrimeHandler(CoreRequestHandler):

    author = "mra"
    title = "prime job handler"

    def get(self):
        return self.post()

    def post(self):
        start = self.get_argument("start", as_type=int, default=None)
        end = self.get_argument("end", as_type=int, default=None)
        size = self.get_argument("size", as_type=int, default=None)
        if None in (start, end, size):
            return self.render("templates/prime.html", job_id=None)
        kwargs = {
            "start": start,
            "end": end,
            "size": size
        }
        job = enqueue("mypro.job.PrimeJobControl", **kwargs)
        if self.wants_html():
            return self.render("templates/prime.html", job_id=str(job._id))
        return self.redirect("http://devops:5002"
                             "/coco/v1/jobs/poll/" + str(job._id))

class PrimeServer(CoreApiContainer):
    rules = [
        (r'/prime', PrimeHandler)
    ]


if __name__ == '__main__':
    from core4.api.v1.tool.functool import serve
    serve(PrimeServer)