import random
import re
import time
import urllib
import asyncio
from asyncio import Task
from collections import namedtuple
from pydantic import BaseModel, Field
import aiohttp
import yarl
from aiohttp import ClientSession
import utils
from utils import time_it, DATE_FORMAT, SupportedWebsite

from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from multiprocessing import Pool
import logging

logger = logging.getLogger(__name__)


class ChapterInfo(BaseModel):
    """Fields
    url: str
    chapter: str
    time: str????
    url_name: str
    favicon_url: str"""
    url: str
    chapter: str
    time: str = None
    url_name: str
    favicon_url: str


class WebHandler:
    # __chapter_pattern = re.compile("[C|c]hapter.{1}[0-9]+\.*[0-9]*")
    # __chapter_pattern = re.compile(" *[C|c]h(apter|\.).{1}[0-9]+\.*[0-9]*")
    __chapter_pattern = re.compile(" *[C|c]h(apter|\.).{1}[0-9]+\.*[0-9]*|[E|e]p.?(isode)?.{1}[0-9]+\.*[0-9]*")
    __favicon_pattern = re.compile("^(shortcut icon|icon)$", re.I)

    @time_it
    def get_last_visited_supported_chapters_from_history(self, supported_urls: list[str],
                                                         history: list[tuple[str, str, str]],
                                                         last_updated_date: str) -> list[tuple[str, str, str]]:
        supported_set = set(supported_urls)
        date_format = DATE_FORMAT
        last_updated_date = datetime.strptime(last_updated_date, date_format)
        result = []
        for target_url in supported_set:
            old = False
            for his in history:
                if datetime.strptime(his[1], date_format) < last_updated_date:
                    # handled all, dont need to check previous history
                    old = True
                    break
                if target_url in his[0]:
                    # last visited is not main page
                    if target_url != his[0] and "chapter" in his[0].lower():
                        result.append((target_url, utils.format_chapter(utils.strip_chapter(his[0])), his[1]))
                        break
                    # last visited is main page
                    # it means that the url in the DB didnt change
                    else:
                        continue
            # if we have bookmark which havent read once,
            # just add some default value so we can start tracking it
            else:
                old = True
            if old:
                result.append((target_url, "Chapter 0", history[0][1]))
        return result

    @staticmethod
    def __get_url_names(urls: list[str]) -> list[str]:
        """Format urls and return domain name"""
        stripped_urls = []
        for url in urls:
            splitted = url.split("/")
            if splitted[2][0] == 'w' and splitted[2][1] == 'w':
                pos = splitted[2].find('.')
                stripped_urls.append(splitted[2][pos + 1:])
            else:
                stripped_urls.append(splitted[2])
        return stripped_urls

    @staticmethod
    def get_diff(bookmarked: list[tuple[str, str, str]], history: list[tuple[str, str, str]],
                 url_names_and_favicon: list[tuple[str, str, str]]) -> list[ChapterInfo]:
        """Returns the difference between last read and new chapters
        Params:
        bookmarked: list[tuple[url, chapter, date]]
        history: list[tuple[url, chapter, date]]
        url_names_and_favicon: list[tuple[url, url_name, favicon_name]]
        Return type:
        ChapterInfo
        """
        # convert data to dict for better integrity
        bookmarked_dict = {url: (chapter, date) for url, chapter, date in bookmarked}
        history_dict = {url: (chapter, date) for url, chapter, date in history}
        names = {url: (name, icon) for url, name, icon in url_names_and_favicon}
        diff = {}
        for url, data in bookmarked_dict.items():
            if url in history_dict:
                if history_dict[url][0] != data[0]:
                    diff[url] = (*data, *names[url])
        return [ChapterInfo(url=url, chapter=data[0], time=data[1], url_name=data[2], favicon_url=data[3]) for url, data
                in diff.items()]

    def get_supported_urls(self, urls) -> list[str]:
        """Returns the list of supported urls"""
        stripped_urls = self.__get_url_names(urls)
        supported = []
        for full, strip in zip(urls, stripped_urls):
            if SupportedWebsite.supported_website(strip):
                supported.append(full)
        return supported

    @time_it
    def get_bookmarked_data(self, urls: list[str]) -> list[ChapterInfo]:
        """Return bookmarked data as a list of tuples with fields:
        url
        chapter
        time
        url_name
        favicon_url"""
        # shuffle to prevent form accessing same website multiple times in a row
        # to reduce the chance of being blocked
        random.shuffle(urls)
        current_time = datetime.now().replace(microsecond=0)
        data = []
        for task in asyncio.run(self.__get_last_chapters(urls)):
            if task.result():
                data.append(
                    ChapterInfo(url=task.result().url, chapter=task.result().chapter, time=str(current_time),
                                url_name=task.result().url_name,
                                favicon_url=task.result().favicon_url))
        return data

    async def __get_last_chapters(self, urls: list[str]) -> list[Task[ChapterInfo]]:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        headers = {"User-Agent": user_agent}
        my_conn = aiohttp.TCPConnector(limit=5)
        async with aiohttp.ClientSession(connector=my_conn, headers=headers) as session:
            tasks = []
            for url in urls:
                task = asyncio.create_task(self.__parse_url(url=url, session=session))
                if task:
                    tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)
        return tasks

    async def __parse_url(self, url: str, session: ClientSession, tries: int = 0) -> ChapterInfo | None:
        """Returns named tuple:
        url
        chapter
        url_name
        favicon_url"""
        # limiter of tries per url
        if tries > 2:
            return
        url = yarl.URL(url, encoded=True)
        async with session.get(url=url) as response:
            result = await response.text()
            try:
                soup = BeautifulSoup(result, "html.parser")
                response_processed = soup.select_one(
                    SupportedWebsite.class_to_find_last_chapter(self.__get_url_names([str(url)])[0]))
                favicon = soup.find('link', attrs={'rel': self.__favicon_pattern}).get('href')
                if "https" not in favicon:
                    favicon = "https://" + self.__get_url_names([str(url)])[0] + favicon
                chapter = re.search(self.__chapter_pattern, response_processed.text).group(0).strip()
            except Exception as e:
                print("Error, probably server blocked request, trying once more")
                logger.error(f"Failed to scrape {str(url)} {tries + 1} times")
                return await self.__parse_url(str(url), session, tries + 1)
            parser_result = ChapterInfo(url=str(url), chapter=chapter, url_name=soup.title.string.strip(),
                                        favicon_url=favicon)
            logger.info(f"Scraped {parser_result}")
            return parser_result
