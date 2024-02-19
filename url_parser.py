from utils import SupportedWebsite


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

    def get_last_chapter(self, urls: list[str]) -> str:
        req = request
