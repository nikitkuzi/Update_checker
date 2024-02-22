import re
import time
import urllib
import asyncio
from asyncio import Task

import aiohttp
from aiohttp import ClientSession

from utils import time_it
from utils import SupportedWebsite

from bs4 import BeautifulSoup
import requests


class UrlParser:
    __pattern = re.compile("[C|c]hapter.{1}[0-9]+\.*[0-9]*")

    def __get_url_names(self, urls: list[str]) -> list[str]:
        stripped_urls = []
        for url in urls:
            splitted = url.split("/")
            if splitted[2][0] == 'w' and splitted[2][1].isalnum() and splitted[2][2].isalnum():
                stripped_urls.append(splitted[2][4:])
            else:
                stripped_urls.append(splitted[2])
        return stripped_urls

    def get_supported_urls(self, urls) -> list[str]:
        stripped_urls = self.__get_url_names(urls)
        supported = []
        for full, strip in zip(urls, stripped_urls):
            if SupportedWebsite.supported_website(strip):
                supported.append(full)
        return supported

    @time_it
    def get_last_chapters_from_url(self, urls: list[str]) -> list[str]:
        return [task.result() for task in asyncio.run(self.__get_last_chapters2(urls))]

    async def __get_last_chapters2(self, urls: list[str]) -> list[Task[[tuple[str,str]]]]:
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

    async def __parse_url(self, url: str, session: ClientSession) -> tuple[str, str]:
        async with session.get(url) as response:
            result = await response.text()
            soup = BeautifulSoup(result, "html.parser")
            curr = soup.find(text=self.__pattern)
            time.sleep(2)
            return url, re.search(self.__pattern, curr).group(0)
