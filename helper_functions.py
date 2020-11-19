import concurrent.futures
import random
import sys
import traceback


# code from https://stackoverflow.com/questions/19309514/how-to-get-correct-line-number-where-exception-was-thrown-using-concurrent-futur/24457608#24457608
class ThreadPoolExecutorStackTraced(concurrent.futures.ThreadPoolExecutor):
    def submit(self, fn, *args, **kwargs):
        """Submits the wrapped function instead of `fn`"""

        return super(ThreadPoolExecutorStackTraced, self).submit(
            self._function_wrapper, fn, *args, **kwargs)

    def _function_wrapper(self, fn, *args, **kwargs):
        """Wraps `fn` in order to preserve the traceback of any kind of
        raised exception

        """
        try:
            return fn(*args, **kwargs)
        except Exception:
            raise sys.exc_info()[0](traceback.format_exc())


def random_decimal(start, stop, decimal_places=2):
    factor = 10 ** decimal_places
    start = int(start * factor)
    stop = int(stop * factor)
    n = random.randint(start, stop)
    return n / factor


def mutate_value(min_value, max_value, current_value, mutation):
    min_mutation = max(min_value, current_value - mutation)
    max_mutation = min(max_value, current_value + mutation)
    return random_decimal(min_mutation, max_mutation)
