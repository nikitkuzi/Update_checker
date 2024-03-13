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

    # bookmarked_data = parser.get_bookmarked_data(supported_urls)
    bookmarked_data = [('https://reaperscans.com/comics/1757-the-rebirth-of-an-8th-circled-wizard', 'Chapter 159', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/5150-sss-class-suicide-hunter', 'Chapter 115', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/6569-the-reincarnated-assassin-is-a-genius-swordsman', 'Chapter 37', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/3893-this-is-the-law', 'Chapter 116', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/2995-perfect-surgeon', 'Chapter 96', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/6198-leveling-with-the-gods', 'Chapter 107', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/4468-the-martial-god-who-regressed-back-to-level-2', 'Chapter 51', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/4050-swordmasters-youngest-son', 'Chapter 100', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/7868-return-of-the-frozen-player', 'Chapter 112', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/6415-rankers-return', 'Chapter 133', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/7655-return-of-the-legendary-spear-knight', 'Chapter 108', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/4073-overgeared', 'Chapter 220', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/3913-hard-carry-support', 'Chapter 52', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/6763-the-100th-regression-of-the-max-level-player', 'Chapter 41.5', '2024-03-12 21:12:36'), ('https://reaperscans.com/comics/9259-barbarian-quest', 'Chapter 100', '2024-03-12 21:12:36')]

    dbbh = BookmarkedHistory()
    # dbbh.reset()
    # dbbh.create(bookmarked_data)
    # dbbh.update(bookmarked_data)
    # print(dbbh.get_last_data())


    dbvh = VisitedHistory()
    # dbvh.reset()
    # dbvh.create(bookmarked_data)
    # print(dbvh.get_last_data())


    last_visited_chapters = parser.get_last_visited_from_history(supported_urls, history, dbvh.get_last_time())

