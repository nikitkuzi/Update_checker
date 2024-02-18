import abc
import typing


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

    @abc.abstractmethod
    def get_bookmarks(self):
        pass

    @abc.abstractmethod
    def get_history(self):
        pass

    @abc.abstractmethod
    @property
    def history_dir(self) -> str:
        pass

    @abc.abstractmethod
    @property
    def bookmarks_dir(self) -> str:
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
