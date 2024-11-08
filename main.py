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

import asyncio

def strip(urls):
    stripped_urls = []
    for url in urls:
        splitted = url.split("/")
        if splitted[2][0] == 'w' and splitted[2][1].isalnum() and splitted[2][2].isalnum():
            stripped_urls.append(splitted[2][4:])
        else:
            stripped_urls.append(splitted[2])
    return stripped_urls

if __name__ == '__main__':
    folders = ['manga11', 'manga', 'manga1', 'manga2', 'manga3', 'manga4', 'manga5', 'manga6', 'manga7']

    browser = Chrome()
    browser.set_bookmark_folders(folders)
    bookmarks = browser.get_bookmarks()
    history = browser.get_history()
    print(bookmarks)
    exit(0)
    parser = WebHandler()
    bookmarked_urls = [bookmark[0] for bookmark in bookmarks]
    supported_urls = parser.get_supported_urls(bookmarked_urls)
    data = parser.get_bookmarked_data(supported_urls)

    # bookmarked_data = [(bookmark.url, bookmark.chapter, bookmark.time) for bookmark in data]
    # bookmarked_names_and_icons = [(bookmark.url, bookmark.url_name, bookmark.favicon_url) for bookmark in data]

    dbbh = BookmarkedHistory()
    # dbbh.reset()
    # dbbh.create(bookmarked_data)
    # dbbh.update(bookmarked_data)
    # print(dbbh.get_last_data())

    dbvh = VisitedHistory()
    # dbvh.reset()
    # dbvh.create(bookmarked_data)
    # print(dbvh.get_last_data())
    # last_visited_chapters = parser.get_last_visited_supported_chapters_from_history(supported_urls, history, dbvh.get_last_time())
    # dbvh.update(last_visited_chapters)

    dbnms = UrlNamesIcons()
    # dbnms.reset()
    # dbnms.create(bookmarked_names_and_icons)
    # print(dbnms.get_last_data())

    to_read = parser.get_diff(dbbh.get_last_data(), dbvh.get_last_data(), dbnms.get_last_data())
    # to_read = parser.get_diff(bookmarked_data, dbvh.get_last_data(), dbnms.get_last_data())
    print(to_read)
