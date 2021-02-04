import concurrent.futures
import sys
import traceback
from enum import Enum


class Speed(Enum):
    SLOW = 0
    NORMAL = 1
    FAST = 2

    def reduce(self):
        return Speed((self.value - 1) % 3)

    def increment(self):
        return Speed((self.value + 1) % 3)


State = Enum("State", "PAUSE RUNNING PLAY ERROR FINISHED CONTINUE")


# code from https://stackoverflow.com/questions/19309514/how-to-get-correct-line-number-where-exception-was-thrown-using-concurrent-futur/24457608#24457608
class ThreadPoolExecutorStackTraced(concurrent.futures.ThreadPoolExecutor):
    def submit(self, fn, *args, **kwargs):
        """Submits the wrapped function instead of `fn`"""

        return super(ThreadPoolExecutorStackTraced, self).submit(
            self._function_wrapper, fn, *args, **kwargs
        )

    def _function_wrapper(self, fn, *args, **kwargs):
        """Wraps `fn` in order to preserve the traceback of any kind of
        raised exception

        """
        try:
            return fn(*args, **kwargs)
        except Exception:
            raise sys.exc_info()[0](traceback.format_exc())
