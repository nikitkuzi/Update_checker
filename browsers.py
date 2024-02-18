import abc
import typing
from email import utils
from pathlib import Path
import platform


class Browser(abc.ABC):
    windows_path: typing.Optional[str]
    mac_path: typing.Optional[str]
    linux_path: typing.Optional[str]

    profile_support: bool
    """Boolean indicating whether the browser supports multiple profiles."""

    profile_dir_prefixes: typing.Optional[typing.List[typing.Any]]
    """List of possible prefixes for the profile directories."""

    bookmarks_file: str
    """Name of the (SQLite, JSON or PLIST) file which stores the bookmarks."""

    history_file: str
    """Name of the (SQLite, JSON or PLIST) file which stores the bookmarks."""

    def __init__(self):
        if not self.supported_platform():
            raise Exception("Not supported platform")

    @classmethod
    def supported_platform(cls):
        supported = ("Windows", "Linux", "Mac OS")
        return platform.system() in supported

    @abc.abstractmethod
    def get_bookmarks(self):
        pass

    @abc.abstractmethod
    def get_history(self):
        pass


class Chrome(Browser):
    """Google Chrome Browser

    Supported platforms:

    * Windows
    * Linux
    * Mac OS

    Profile support: Yes
    """

    __name = "Chrome"

    __linux_path = ".config/google-chrome"
    __windows_path = "AppData/Local/Google/Chrome/User Data"
    __mac_path = "Library/Application Support/Google/Chrome/"

    __profile_support = True
    __profile_dir_prefixes = ["Default*", "Profile*"]

    __history_file = "History"
    __bookmarks_file = "Bookmarks"

    __history_dir = "asd"
    __bookmarks_dir = ""

    def get_bookmarks(self):
        pass

    def get_history(self):
        return self.__history_dir

    def history_dir(self) -> str:
        return ""
