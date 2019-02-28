from core4.api.v1.request.main import CoreRequestHandler
from core4.queue.helper.functool import enqueue
from mypro.job import PrimeJob


class PrimeHandler(CoreRequestHandler):
    author = "mra"
    title = "prime job handler"

    async def get(self):
        """
        Same as :meth:`.post`
        """
        return await self.post()

    async def post(self):
        """
        Identify and store prime number in mongo collection ``prime`` from
        ``start`` to ``end`` using chunks of ``size``.
        """
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
        job = enqueue(PrimeJob, **kwargs)
        if self.wants_html():
            return self.render("templates/prime.html", job_id=str(job._id))
        url = await self.reverse_url("JobStream", str(job._id))
        return self.redirect(url)

# http://devops:5001/core4/api/enter/bc8c3f196df700db3d1420a4d5a4d3b5?start=1&end=10000&size=500&content_type=json