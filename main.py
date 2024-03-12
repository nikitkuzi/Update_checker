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

    # url_and_last_chapters = parser.get_last_chapters_from_url(supported_urls)
    url_and_last_chapters = [('https://reaperscans.com/comics/9259-barbarian-quest', 'Chapter 97'), (
        'https://reaperscans.com/comics/6763-the-100th-regression-of-the-max-level-player', 'Chapter 41.5'),
                             ('https://reaperscans.com/comics/4073-overgeared', 'Chapter 218'),
                             ('https://reaperscans.com/comics/2995-perfect-surgeon', 'Chapter 95'), (
                                 'https://reaperscans.com/comics/1757-the-rebirth-of-an-8th-circled-wizard',
                                 'Chapter 160'),
                             ('https://reaperscans.com/comics/3913-hard-carry-support', 'Chapter 52'), (
                                 'https://reaperscans.com/comics/7655-return-of-the-legendary-spear-knight',
                                 'Chapter 108'),
                             ('https://reaperscans.com/comics/5150-sss-class-suicide-hunter', 'Chapter 113'),
                             ('https://reaperscans.com/comics/3893-this-is-the-law', 'Chapter 115'),
                             ('https://reaperscans.com/comics/7868-return-of-the-frozen-player', 'Chapter 110'), (
                                 'https://reaperscans.com/comics/4468-the-martial-god-who-regressed-back-to-level-2',
                                 'Chapter 49'),
                             ('https://reaperscans.com/comics/6198-leveling-with-the-gods', 'Chapter 105.5'), (
                                 'https://reaperscans.com/comics/6569-the-reincarnated-assassin-is-a-genius-swordsman',
                                 'Chapter 34'),
                             ('https://reaperscans.com/comics/4050-swordmasters-youngest-son', 'Chapter 100'),
                             ('https://reaperscans.com/comics/6415-rankers-return', 'Chapter 132')]
    # print(url_and_last_chapters)
    dbbh = BookmarkedHistory()
    # dbbh.reset()
    # dbbh.create(url_and_last_chapters)
    # print(dbbh.get_last_data())

    # last_visited_urls_with_date = parser.get_last_visited_urls_with_date(supported_urls, history)
    # print(last_visited_urls_with_date)

    date_now = datetime.now().replace(microsecond=0)
    url_and_last_chapters_with_dates = [(url, chapter, date_now) for url, chapter in url_and_last_chapters]

    dbvh = VisitedHistory()
    # dbvh.reset()
    # dbvh.create(url_and_last_chapters_with_dates)
    print(dbvh.get_last_data())
    # print(dbvh.get_last_time())

    # todo if url is equal to bookmarked
    last_visited_chapters = parser.get_last_visited_from_history(supported_urls, history, dbvh.get_last_time())
    print(last_visited_chapters)
    dbvh.update(last_visited_chapters)
    print(dbvh.get_last_data())

    # print(utils.strip_chapter(last_visited_chapters[0][0]))
