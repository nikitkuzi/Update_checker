import platform
import time

class SupportedWebsite:
    __supported = {"reaperscans.com"}
    @classmethod
    def supported_website(cls, url: str) -> bool:
        return url in cls.__supported


def time_it(func):
    def wrapper(*args, **kwargs):
        curr_time = time.time()
        res = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - curr_time}ms to run")
        return res

    return wrapper
