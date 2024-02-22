import re
import time
import urllib
import asyncio
import aiohttp

from utils import time_it
from utils import SupportedWebsite

from bs4 import BeautifulSoup
import requests


class UrlParser:

    def __get_url_names(self, urls: list[str]) -> list[str]:
        stripped_urls = []
        for url in urls:
            splitted = url.split("/")
            if splitted[2][0] == 'w' and splitted[2][1].isalnum() and splitted[2][2].isalnum():
                stripped_urls.append(splitted[2][4:])
            else:
                stripped_urls.append(splitted[2])
        return stripped_urls

    def get_supported(self, urls) -> list[str]:
        stripped_urls = self.__get_url_names(urls)
        supported = []
        for full, strip in zip(urls, stripped_urls):
            if SupportedWebsite.supported_website(strip):
                supported.append(full)
        return supported

    @time_it
    def get_last_chapters1(self, urls: list[str]) -> list[str]:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        headers = {"User-Agent": user_agent}
        chapters = []
        pattern = re.compile("[Cc]hapter.+[0-9]")
        for url in urls:
            req = requests.get(url, headers=headers)
            soup = BeautifulSoup(req.text, "html.parser")
            curr = soup.find(text=pattern)
            print(curr)
            chapters.append(re.search(pattern, curr).group(0))
            time.sleep(0.5)
        return chapters

    @time_it
    def get_last_chapters(self, urls: list[str]) -> list[str]:
        return asyncio.run(self.__get_last_chapters2(urls))

    async def __get_last_chapters2(self, urls: list[str]) -> list[str]:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        headers = {"User-Agent": user_agent}
        my_conn = aiohttp.TCPConnector(limit=5)
        async with aiohttp.ClientSession(connector=my_conn, headers=headers) as session:
            tasks = []
            for url in urls:
                task = asyncio.ensure_future(self.__parse_url(url=url, session=session))
                # print(task.result())
                tasks.append(task)
            await asyncio.gather(*tasks, return_exceptions=True)  # the await must be nest inside of the session
        return tasks

    async def __parse_url(self, url: str, session) -> str:
        async with session.get(url) as response:
            result = await response.text()
            time.sleep(1)
            pattern = re.compile("[Cc]hapter.+[0-9]")
            soup = BeautifulSoup(result, "html.parser")
            curr = soup.find(text=pattern)
            # print(curr, result)
            return re.search(pattern, curr).group(0)
