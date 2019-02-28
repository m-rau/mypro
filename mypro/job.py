import math

from pymongo.errors import DuplicateKeyError

from core4.queue.helper.functool import enqueue
from core4.queue.helper.job.base import CoreLoadJob


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
    defer_time = 5
    max_parallel = 3

    def execute(self, start=None, end=None, size=None, mid=None, count=None,
                **kwargs):
        if size:
            if self.trial == 1:
                # launching
                for i in range(start, end, size):
                    e = i + size
                    if e > end:
                        e = end
                    enqueue(PrimeJob, start=i, end=e, mid=str(self._id),
                            **kwargs)
                self.defer("waiting")
            # monitoring
            running = self.config.sys.queue.count_documents(
                {"args.mid": str(self._id)})
            if running > 0:
                total = float(math.ceil((end - start + 1) / size))
                p = 1. - running / total
                self.progress(p, "%d of %d running", running, total)
                self.defer("check %f: waiting for %d of %d jobs to complete",
                           p, running, total)
            self.logger.info("check: seen all jobs complete")
            return

        # calculating
        coll = self.config.mypro.prime_collection
        self.set_source(self.started_at.isoformat())
        n = 0
        for i in range(start, end):
            if check_prime(i):
                n += 1
                try:
                    coll.insert_one({"_id": i})
                except DuplicateKeyError:
                    pass
                except:
                    raise
            self.progress(i / end)
        self.logger.debug("found [%d] primes", n)

if __name__ == '__main__':
    from core4.queue.helper.functool import execute
    execute(PrimeJob, start=1, end=3000000, size=500000)
    # execute(PrimeJob, start=1, end=100000, mid="5c7445f0ad7071140796f3c6")
