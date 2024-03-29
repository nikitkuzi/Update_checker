import platform
import time
import re

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


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


def strip_chapter(chapter: str) -> str:
    return re.search("[C|c]hapter.{1}[0-9]+\.*[0-9]*", chapter).group(0)


def format_chapter(chapter: str) -> str:
    return chapter.replace('-', ' ').replace('  ', ' ').capitalize()
