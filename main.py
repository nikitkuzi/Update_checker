from datetime import datetime, timedelta

import utils
from browsers import Chrome
from web_handler import WebHandler
from browser_history.generic import Browser
from db_handler import BookmarkedHistory, VisitedHistory
from utils import DATE_FORMAT

import time

import asyncio

if __name__ == '__main__':
    folders = ['manga', 'manga1', 'manga2', 'manga3', 'manga4']

    browser = Chrome()
    browser.set_bookmark_folders(folders)
    bookmarks = browser.get_bookmarks()
    history = browser.get_history()

    parser = WebHandler()
    bookmarked_urls = [bookmark[0] for bookmark in bookmarks]
    supported_urls = parser.get_supported_urls(bookmarked_urls)

    last_visited_urls_with_date = parser.get_last_visited_urls_with_date(supported_urls, history)
    print(last_visited_urls_with_date)
    dbvh = VisitedHistory()
    # dbvh.reset()
    # dbvh.create(last_visited_urls_with_date)
    # print(dbvh.get_last_data())
    # print(dbvh.get_last_time())

    # url_and_last_chapters = parser.get_last_chapters_from_url(supported_urls)
    # print(url_and_last_chapters)
    dbbh = BookmarkedHistory()
    # dbbh.reset()
    # dbbh.create(url_and_last_chapters)
    # print(dbbh.get_last_data())

    last_visited_chapters = parser.get_last_visited_from_history(supported_urls, history, dbvh.get_last_time())
    print(last_visited_chapters)
