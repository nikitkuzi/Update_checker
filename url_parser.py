import re
import time
import urllib

from utils import SupportedWebsite
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

    def get_supported(self, urls):
        stripped_urls = self.__get_url_names(urls)
        supported = []
        for full, strip in zip(urls, stripped_urls):
            if SupportedWebsite.supported_website(strip):
                supported.append(full)
        return supported

    def get_last_chapters(self, urls: list[str]) -> list[str]:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        headers = {"User-Agent":user_agent}
        chapters = []
        for url in urls:
            req = requests.get(url,headers=headers)
            chapters.append(re.search("Chapter.+[0-9]", req.text).group(0))
            time.sleep(1)
            break
        return chapters
