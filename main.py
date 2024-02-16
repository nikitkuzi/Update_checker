import os
import json
import sqlite3
from typing import Callable
from browser_history.browsers import Chrome
import platform

def load_user_bookmarks(folders: set[str]):
    """Load user bookmarks"""
    with open(get_path('Bookmarks'), encoding='utf-8') as file:
        data = json.load(file)

    urls = []

    for folder in data['roots']['bookmark_bar']['children']:
        if folder['name'] in folders:
            for bookmark in folder['children']:
                urls.append(bookmark['url'])


def get_path(filename: str) -> str:
    """Returns path to filename from chrome user default folder"""
    current_system = platform.system()
    if current_system == "Linux":
        return os.path.join(os.path.expanduser('~'),".config/google-chrome/Default", filename)
    elif current_system == "Windows":
        return os.path.join(os.getenv('LOCALAPPDATA'), r'Google\Chrome\User Data\Default', filename)
    else:
        raise Exception("Non supported OS")


def get_history(browser: Callable):
    outputs = browser().fetch_history(desc=True)
    history = [hstr[1] for hstr in outputs.histories]

    print(history[:20])


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
    load_user_bookmarks(folders)
    get_history(Chrome)
    # get_bookmarks(folders)
