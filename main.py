from browsers import Chrome
from url_parser import UrlParser
from browser_history.generic import Browser
from db_handler import Bookmarked, History
from utils import strip_chapter

import time

import asyncio



if __name__ == '__main__':
    folders = ['manga', 'manga1', 'manga2', 'manga3', 'manga4']

    browser = Chrome()
    browser.set_bookmark_folders(folders)
    bookmarks = browser.get_bookmarks()
    history = browser.get_history()

    parser = UrlParser()
    test = [visited[0] for visited in bookmarks]

    supported = parser.get_supported(test)

    supported_history_set = set(supported)
    last_visited = []
    for i in range(len(history)):
        if not supported_history_set:
            break
        if history[i][0] in supported_history_set:
            supported_history_set.remove(history[i][0])
            last_visited.append(history[i][:2])
    # print(last_visited)
    # for _ in range(1):
    #     last_chapters = parser.get_last_chapters(supported[:3])
    #     time.sleep(10)
    # print(last_chapters)
    # print(supported)
    last_chapters = parser.get_last_chapters(supported)
        # time.sleep(10)
    print(last_chapters)
    # last_chapters = ['Chapter 217', 'Chapter 94', 'Chapter 110', 'Chapter 132', 'Chapter 108', 'Chapter 160', 'Chapter 112.5', 'Chapter 114', 'Chapter 100 - Season 1', 'Chapter 105.5', 'Chapter 97', 'Chapter 52', 'Chapter 41.5', 'Chapter 48', 'Chapter 34']



    # values = tuple(zip(supported,last_chapters))
    # # values = tuple([('https://reaperscans.com/comics/4073-overgeared', 'Chapter 217'), ('https://reaperscans.com/comics/2995-perfect-surgeon', 'Chapter 94'), ('https://reaperscans.com/comics/7868-return-of-the-frozen-player', 'Chapter 110')])
    # print(values)
    #
    # db = History()
    # db.reset()
    # db.create(last_visited)
    # print(db.get_last_data())
    # print(db.get_last_time())
