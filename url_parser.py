class UrlParser:

    def get_url_names(self, urls: list[str]) -> list[str]:
        stripped_urls = []
        for url in urls:
            splitted = url.split("/")
            if splitted[2][0] == 'w' and splitted[2][1].isalnum() and splitted[2][2].isalnum():
                stripped_urls.append(splitted[2][4:])
            else:
                stripped_urls.append(splitted[2])
        return stripped_urls

