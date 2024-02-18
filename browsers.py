import abc
import os
import typing
from email import utils
from pathlib import Path
import platform


class Browser(abc.ABC):
    __windows_path: typing.Optional[str]
    __mac_path: typing.Optional[str]
    __linux_path: typing.Optional[str]

    __profile_support: bool
    """Boolean indicating whether the browser supports multiple profiles."""

    __profile_dir_prefixes: typing.Optional[typing.List[typing.Any]]
    """List of possible prefixes for the profile directories."""

    __bookmarks_file: str
    """Name of the (SQLite, JSON or PLIST) file which stores the bookmarks."""

    __history_file: str
    """Name of the (SQLite, JSON or PLIST) file which stores the bookmarks."""

    def __init__(self):
        if not self.supported_platform():
            raise Exception("Not supported platform")

        self.set_history_path()
        self.set_bookmarks_path()

    @classmethod
    def supported_platform(cls) -> bool:
        supported = ("Windows", "Linux", "Mac OS")
        return platform.system() in supported

    @abc.abstractmethod
    def get_bookmarks(self):
        pass

    @abc.abstractmethod
    def get_history(self):
        pass

    @abc.abstractmethod
    def set_history_path(self):
        pass

    @abc.abstractmethod
    def set_bookmarks_path(self):
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
    __profile_dir_prefixes = ["Default", "Profile"]

    __history_file = "History"
    __bookmarks_file = "Bookmarks"

    __platform = platform.system()

    def get_bookmarks(self):
        pass

    def get_history(self):
        pass

    def set_history_path(self):
        d = os.listdir(os.path.join(os.path.expanduser('~'),self.__linux_path, self.__profile_dir_prefixes[0]))
        print(sorted(d))

    def set_bookmarks_path(self):
        pass
