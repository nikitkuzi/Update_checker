from utils import SupportedWebsite


class UrlParser:

    def get_url_names(self, urls: list[str]) -> list[str]:
        stripped_urls = []
        for url in urls:
            splitted = url.split("/")
            if splitted[2][0] == 'w' and splitted[2][1].isalnum() and splitted[2][2].isalnum():
                stripped_urls.append(splitted[2][4:])
            else:
                stripped_urls.append(splitted[2])
        print(self.get_supported(stripped_urls))
        return stripped_urls

    def get_supported(self, urls):
        return list(filter(SupportedWebsite.supported_website, urls))
