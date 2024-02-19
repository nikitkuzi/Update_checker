from browsers import Chrome
from url_parser import UrlParser
from utils import SupportedWebsite
from db_handler import DbHandler

import time
from browser_history.generic import Browser


def time_it(func):
    def wrapper(*args, **kwargs):
        curr_time = time.time()
        res = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - curr_time}ms to run")
        return res

    return wrapper


if __name__ == '__main__':
    folders = ['manga', 'manga1', 'manga2', 'manga3', 'manga4']

    b = Chrome()
    b.set_bookmark_folders(folders)
    bookmarks = b.get_bookmarks()
    history = b.get_history()

    parser = UrlParser()
    test = [visited[0] for visited in bookmarks]

    supported = parser.get_supported(test)
    # print(supported)

    last_chapters = parser.get_last_chapters(supported)
    print(last_chapters, supported)


    # db = DbHandler()

