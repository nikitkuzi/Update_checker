from browsers import Chrome
from url_parser import UrlParser
from utils import SupportedWebsite
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
    parsed = parser.get_url_names(test)
    # print(UrlParser.get_supported(parsed))


