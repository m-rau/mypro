import math

from core4.queue.helper.job.base import CoreLoadJob
from core4.queue.helper.functool import enqueue


def check_prime(n):
    if n % 2 == 0:
        return False
    from_i = 3
    to_i = math.sqrt(n) + 1
    for i in range(from_i, int(to_i), 2):
        if n % i == 0:
            return False
    return True


class PrimeJob(CoreLoadJob):
    author = "mra"

    def execute(self, start, end, size=None, **kwargs):
        if size:
            for i in range(start, end, size):
                e = i + size
                if e > end:
                    e = end
                enqueue(PrimeJob, start=i, end=e, **kwargs)
            return
        for i in range(start, end):
            self.progress(i/end)
            if check_prime(i):
                print("found [%d]" %(i))
                self.logger.info("found [%d]", i)


class PrimeJobControl(CoreLoadJob):
    author = "mra"
    defer_time = 5
    max_parallel = 3

    def execute(self, start=None, end=None, size=None, mid=None, count=None,
                **kwargs):
        if size:
            if self.trial > 1:
                running = self.config.sys.queue.count_documents(
                    {"args.mid": str(self._id)})
                if running > 0:
                    self.defer("check: waiting for %d jobs to complete", running)
                self.logger.info("check: seen all jobs complete")
                return
            for i in range(start, end, size):
                e = i + size
                if e > end:
                    e = end
                enqueue(PrimeJobControl, start=i, end=e, mid=str(self._id),
                        **kwargs)
            self.defer("waiting")
        else:
            for i in range(start, end):
                self.progress(i/end)
                if check_prime(i):
                    print("found [%d]" %(i))
                    self.logger.info("found [%d]", i)


if __name__ == '__main__':
    from core4.queue.helper.functool import execute
    execute(PrimeJobControl, start=1, end=3000000, size=500000)
