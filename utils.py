import platform


class SupportedWebsite:
    __supported = {"reaperscans.com"}
    @classmethod
    def supported_website(cls, url: str) -> bool:
        return url in cls.__supported
