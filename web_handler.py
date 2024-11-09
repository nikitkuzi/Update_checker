import random
import re
import time
import urllib
import asyncio
from asyncio import Task
from collections import namedtuple

import aiohttp
import yarl
from aiohttp import ClientSession

import utils
from utils import time_it, DATE_FORMAT, SupportedWebsite

from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from multiprocessing import Pool


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
        result = []
        for target_url in supported_set:
            for his in history:
                if datetime.strptime(his[1], date_format) < datetime.strptime(last_updated_date, date_format):
                    # handled all, dont need to check previous history
                    break
                if target_url in his[0]:
                    # last visited is not main page
                    if target_url != his[0] and "chapter" in his[0].lower():
                        result.append((target_url, utils.format_chapter(utils.strip_chapter(his[0])), his[1]))
                    # last visited is main page
                    # it means that the url in the DB didnt change
                    else:
                        continue
                    break
        return result

    def __get_url_names(self, urls: list[str]) -> list[str]:
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

    def get_diff(self, bookmarked: list[tuple[str, str, str]], history: list[tuple[str, str, str]],
                 names_list: list[tuple[str, str]]) -> list[
        tuple[str, str, str, str, str]]:
        """Returns the difference between last read and new chapters as a list of tuples with fields:
        url
        chapter
        time
        url_name
        favicon_url
        """
        new = {url: (chapter, date) for url, chapter, date in bookmarked}
        old = {url: (chapter, date) for url, chapter, date in history}
        names = {url: (name, icon) for url, name, icon in names_list}
        diff = {}
        for url, data in new.items():
            if url in old:
                if old[url][0] != data[0]:
                    diff[url] = (*data, *names[url])
        return [(url, *data) for url, data in diff.items()]

    def get_supported_urls(self, urls) -> list[str]:
        """Returns the list of supported"""
        stripped_urls = self.__get_url_names(urls)
        supported = []
        for full, strip in zip(urls, stripped_urls):
            if SupportedWebsite.supported_website(strip):
                supported.append(full)
        return supported

    # def get_last_visited_urls_with_date(self, supported_urls: list[str], history: list[tuple[str, str, str]]) -> list[
    #     tuple[str, str, str]]:
    #     supported_history_set = set(supported_urls)
    #     last_visited = []
    #     default_date_for_url_not_found_in_history = (datetime.now().replace(microsecond=0) - timedelta(days=365)).strftime(
    #         DATE_FORMAT)
    #     for i in range(len(history)):
    #         if not supported_history_set:
    #             # handled all
    #             break
    #         if history[i][0] in supported_history_set:
    #             supported_history_set.remove(history[i][0])
    #             last_visited.append((history[i][0], "", history[i][1]))
    #     # if there are some bookmarked urls which are not in browser history
    #     # just add them with some default value
    #     for url in supported_history_set:
    #         last_visited.append((url, "", default_date_for_url_not_found_in_history))
    #     return last_visited

    @time_it
    def get_bookmarked_data(self, urls: list[str]) -> list[tuple[str, str, str, str, str]]:
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
        # return [(task.result()[0], task.result()[1], str(current_time), task.result()[2], task.result()[3]) for task in
        #         asyncio.run(self.__get_last_chapters2(urls)) if
        #         task.result()[1] != ""]
        data = []
        Bookmark = namedtuple("Bookmark", ["url", "chapter", "time", "url_name", "favicon_url"])
        for task in asyncio.run(self.__get_last_chapters(urls)):
            if task.result():
                data.append(
                    Bookmark(task.result().url, task.result().chapter, str(current_time), task.result().url_name,
                             task.result().favicon_url))
        return data

    async def __get_last_chapters(self, urls: list[str]) -> list[Task[[tuple[str, str]]]]:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        headers = {"User-Agent": user_agent}
        my_conn = aiohttp.TCPConnector(limit=5)
        async with aiohttp.ClientSession(connector=my_conn, headers=headers) as session:
            tasks = []
            for url in urls:
                task = asyncio.create_task(self.__parse_url(url=url, session=session))
                # print(task.result())
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)
        return tasks

    async def __parse_url(self, url: str, session: ClientSession, tries: int = 0) -> tuple[str, str, str, str]:
        """Returns named tuple:
        url
        chapter
        url_name
        favicon_url"""
        # limiter of tries per url
        if tries > 2:
            return
        url = yarl.URL(url, encoded=True)
        Result = namedtuple("Result", ["url", "chapter", "url_name", "favicon_url"])
        async with session.get(url=url) as response:
            print(response.status, url)
            await asyncio.sleep(1)

            result = await response.text()
            try:
                soup = BeautifulSoup(result, "html.parser")
                curr = soup.select_one(SupportedWebsite.class_to_find_last_chapter(self.__get_url_names([str(url)])[0]))

                favicon = soup.find('link', attrs={'rel': self.__favicon_pattern}).get('href')
                if "https" not in favicon:
                    favicon = "https://" + self.__get_url_names([str(url)])[0] + favicon
                res = re.search(self.__chapter_pattern, curr.text).group(0).strip()
            except Exception as e:
                res = ""
                print("Error, probably server blocked request, trying once more")
                return await self.__parse_url(str(url), session, tries + 1)

            # return url, res, soup.title.string, favicon
            return Result(str(url), res, soup.title.string.strip(), favicon)
