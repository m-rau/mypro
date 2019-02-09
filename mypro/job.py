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


if __name__ == '__main__':
    from core4.queue.helper.functool import execute
    execute(PrimeJob, start=1, end=1000000)
