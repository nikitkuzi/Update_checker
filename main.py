from collections import Counter
from datetime import datetime, timedelta

import requests

import utils
from browsers import Chrome
from web_handler import WebHandler
from browser_history.generic import Browser
from db_handler import BookmarkedHistory, VisitedHistory, UrlNamesIcons
from utils import DATE_FORMAT
from fastapi import FastAPI
import time
import logging

import asyncio




def strip(urls):
    stripped_urls = []
    for url in urls:
        splitted = url.split("/")
        if splitted[2][0] == 'w' and splitted[2][1] == 'w':
            pos = splitted[2].find('.')
            stripped_urls.append(splitted[2][pos+1:])
        else:
            stripped_urls.append(splitted[2])
    return stripped_urls

if __name__ == '__main__':
    # config
    folders = ['manga11', 'manga', 'manga1', 'manga2', 'manga3', 'manga4', 'manga5', 'manga6', 'manga7']
    logger = logging
    logger.basicConfig(filename='log.log', level=logging.DEBUG,
                       format='%(levelname)s: %(name)s - %(asctime)s - %(message)s', datefmt='%d/%b/%y %H:%M:%S')
    browser = Chrome()
    browser.set_bookmark_folders(folders)
    bookmarks = browser.get_bookmarks()
    history = browser.get_history()

    parser = WebHandler()
    bookmarked_urls = [bookmark[0] for bookmark in bookmarks]
    # print(Counter(strip(bookmarked_urls)))
    supported_urls = parser.get_supported_urls(bookmarked_urls)

    data = parser.get_bookmarked_data(supported_urls)

    # create dbs
    bookmarked_data = [(bookmark.url, bookmark.chapter, bookmark.time) for bookmark in data]
    bookmarked_names_and_icons = [(bookmark.url, bookmark.url_name, bookmark.favicon_url) for bookmark in data]
    print(bookmarked_data)

    dbbh = BookmarkedHistory()
    # dbbh.reset()
    # dbbh.create(bookmarked_data)
    dbbh.update(bookmarked_data)
    print(dbbh.get_last_data())
    exit(0)
    dbvh = VisitedHistory()
    # dbvh.reset()
    # dbvh.create(bookmarked_data)
    print(dbvh.get_last_data())
    last_visited_chapters = parser.get_last_visited_supported_chapters_from_history(supported_urls, history, dbvh.get_last_time())
    print(last_visited_chapters)
    # dbvh.update(last_visited_chapters)
    # dbvh.update([('https://ww3.mangakakalot.tv/manga/manga-ak977919', 'Chapter 89', '2024-10-10 12:57:41')])


    dbnms = UrlNamesIcons()
    # dbnms.reset()
    # dbnms.create(bookmarked_names_and_icons)
    # print(dbnms.get_last_data())

    to_read = parser.get_diff(dbbh.get_last_data(), dbvh.get_last_data(), dbnms.get_last_data())
    print(to_read)
