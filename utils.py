import platform
import time
import re

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class SupportedWebsite:
    __supported = {"chapmanganato.to", "reaperscans.com"}
    __class_to_find_last_chapter = {"chapmanganato.to": "chapter-name text-nowrap"}
    #    req = requests.get("https://api.reaperscans.com/chapter/query?page=1&perPage=30&query=&order=desc&series_id=162")

    @classmethod
    def supported_website(cls, url: str) -> bool:
        return url in cls.__supported

    @classmethod
    def class_to_find_last_chapter(cls, url: str) -> str:
        return cls.__class_to_find_last_chapter[url]


def time_it(func):
    def wrapper(*args, **kwargs):
        curr_time = time.time()
        res = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - curr_time}ms to run")
        return res

    return wrapper


def strip_chapter(chapter: str) -> str:
    """Returns chapter and its number"""
    return re.search("[C|c]hapter.{1}[0-9]+\.*[0-9]*", chapter).group(0)


def format_chapter(chapter: str) -> str:
    """Removes dashes and spaces from the given chapter"""
    return chapter.replace('-', ' ').replace('  ', ' ').capitalize()
