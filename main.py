import os
import json
import sqlite3
import time
from typing import Callable
from browser_history.browsers import Chrome
import platform
from browsers import Chrome


def time_it(func):
    def wrapper(*args, **kwargs):
        curr_time = time.time()
        res = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - curr_time}ms to run")
        return res

    return wrapper

@time_it
def load_user_bookmarks(folders: set[str]):
    """Load user bookmarks"""
    try:
        with open(get_path('Bookmarks'), encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        raise e

    bookmarks_urls = []

    for folder in data['roots']['bookmark_bar']['children']:
        if folder['name'] in folders:
            for bookmark in folder['children']:
                bookmarks_urls.append(bookmark['url'])
    print(bookmarks_urls)


def get_path(filename: str) -> str:
    """Returns path to filename from chrome user default folder."""
    current_system = platform.system()
    if current_system == "Linux":
        return os.path.join(os.path.expanduser('~'), ".config/google-chrome/Default", filename)
    elif current_system == "Windows":
        return os.path.join(os.getenv('LOCALAPPDATA'), r'Google\Chrome\User Data\Default', filename)
    else:
        raise Exception("Non supported OS")


def get_history(browser: Callable):
    outputs = browser().fetch_history(desc=True)
    history = [hstr[1] for hstr in outputs.histories]

    print(len(history), history[:20])


@time_it
def get_bookmarks(browser: Callable, folders: set[str]):
    outputs = browser().fetch_bookmarks()
    bookmarks = outputs.bookmarks

    urls = []
    for bookmark in bookmarks:
        if any([bookmark[3].endswith(folder) for folder in folders]):
            urls.append(bookmark[1])
    print(urls)


def load_visited_pages():
    pass


if __name__ == '__main__':
    folders = {'manga', 'manga1', 'manga2', 'manga3', 'manga4'}
    # load_user_bookmarks(folders)
    # get_history(Chrome)
    # get_bookmarks(Chrome, folders)
    # a = Chrome()
    b = Chrome()