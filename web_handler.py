import random
import re
import time
import urllib
import asyncio
from asyncio import Task

import aiohttp
from aiohttp import ClientSession

import utils
from utils import time_it, DATE_FORMAT, SupportedWebsite

from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from multiprocessing import Pool


class WebHandler:
    __chapter_pattern = re.compile("[C|c]hapter.{1}[0-9]+\.*[0-9]*")
    __favicon_pattern = re.compile("^(shortcut icon|icon)$", re.I)

    @time_it
    def get_last_visited_from_history(self, supported_urls: list[str], history: list[tuple[str, str, str]],
                                      last_updated_date: str) -> list[tuple[str, str, str]]:
        supported_set = set(supported_urls)
        date_format = DATE_FORMAT
        result = []
        for target_url in supported_set:
            for his in history:
                if datetime.strptime(his[1], date_format) < datetime.strptime(last_updated_date, date_format):
                    break
                if target_url in his[0]:
                    # last visited is not main page
                    if target_url != his[0] and "chapter" in his[0].lower():
                        result.append((target_url, utils.format_chapter(utils.strip_chapter(his[0])), his[1]))
                    # last visited is main page
                    else:
                        continue
                    break
        return result

    def __get_url_names(self, urls: list[str]) -> list[str]:
        stripped_urls = []
        for url in urls:
            splitted = url.split("/")
            if splitted[2][0] == 'w' and splitted[2][1].isalnum() and splitted[2][2].isalnum():
                stripped_urls.append(splitted[2][4:])
            else:
                stripped_urls.append(splitted[2])
        return stripped_urls

    def get_diff(self, bookmarked: list[tuple[str, str, str]], history: list[tuple[str, str, str]],
                 names_list: list[tuple[str, str]]) -> list[
        tuple[str, str, str, str]]:
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
        stripped_urls = self.__get_url_names(urls)
        supported = []
        for full, strip in zip(urls, stripped_urls):
            if SupportedWebsite.supported_website(strip):
                supported.append(full)
        return supported

    def get_last_visited_urls_with_date(self, supported_urls: list[str], history: list[tuple[str, str, str]]) -> list[
        tuple[str, str, str]]:
        supported_history_set = set(supported_urls)
        last_visited = []
        date_for_url_not_found_in_history = (datetime.now().replace(microsecond=0) - timedelta(days=365)).strftime(
            DATE_FORMAT)
        for i in range(len(history)):
            if not supported_history_set:
                break
            if history[i][0] in supported_history_set:
                supported_history_set.remove(history[i][0])
                last_visited.append((history[i][0], "", history[i][1]))
        # if there are some bookmarked urls which are not in browser history
        # just add them with some default value
        for url in supported_history_set:
            last_visited.append((url, "", date_for_url_not_found_in_history))
        return last_visited

    @time_it
    def get_bookmarked_data(self, urls: list[str]) -> list[tuple[str, str, str, str]]:
        # shuffle to prevent form accessing same website multiple times in a row
        # to reduce the chance of being blocked
        random.shuffle(urls)
        curr_time = datetime.now().replace(microsecond=0)
        return [(task.result()[0], task.result()[1], str(curr_time), task.result()[2], task.result()[3]) for task in
                asyncio.run(self.__get_last_chapters2(urls)) if
                task.result()[1] != ""]

    async def __get_last_chapters2(self, urls: list[str]) -> list[Task[[tuple[str, str]]]]:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        headers = {"User-Agent": user_agent}
        my_conn = aiohttp.TCPConnector(limit=2)
        async with aiohttp.ClientSession(connector=my_conn, headers=headers) as session:
            tasks = []
            for url in urls:
                task = asyncio.ensure_future(self.__parse_url(url=url, session=session))
                # print(task.result())
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)
        return tasks

    async def __parse_url(self, url: str, session: ClientSession) -> tuple[str, str, str, str]:
        async with session.get(url) as response:
            result = await response.text()
            soup = BeautifulSoup(result, "html.parser")
            curr = soup.find(text=self.__chapter_pattern)
            favicon = soup.find_all('link', attrs={'rel': self.__favicon_pattern})[0].get('href')
            time.sleep(2)
            try:
                res = re.search(self.__chapter_pattern, curr).group(0)
            except Exception as e:
                res = ""
                print(e)
            return url, res, soup.title.string, favicon
