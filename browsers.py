import abc
import json
import os
import shutil
import typing
import sqlite3
from pathlib import Path
import platform


class Browser(abc.ABC):
    __platform_paths: dict[str, typing.Union[str | None]]
    # __windows_path: typing.Optional[str]
    # __mac_path: typing.Optional[str]
    # __linux_path: typing.Optional[str]

    __profile_support: bool
    """Boolean indicating whether the browser supports multiple profiles."""

    __current_profile: typing.Optional[str]
    """List of possible prefixes for the profile directories."""

    __bookmarks_file: str
    """Name of the (SQLite, JSON or PLIST) file which stores the bookmarks."""

    __history_file: str
    """Name of the (SQLite, JSON or PLIST) file which stores the bookmarks."""

    __path_to_history: str
    __path_to_bookmarks: str

    __bookmark_folders: list[str]
    """Name of folders which contains all of the needed bookmarks"""

    def __init__(self):
        if not self._supported_platform():
            raise Exception("Not supported platform")

        self._set_path()

    @classmethod
    def _supported_platform(cls) -> bool:
        supported = ("Windows", "Linux", "Mac OS")
        return platform.system() in supported

    @abc.abstractmethod
    def set_bookmark_folders(self, folders: list[str]) -> None:
        pass

    @abc.abstractmethod
    def get_bookmarks(self) -> list[tuple[str, str]]:
        pass

    @abc.abstractmethod
    def get_history(self) -> list[tuple[str, str, str]]:
        pass

    @abc.abstractmethod
    def _set_path(self) -> None:
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

    __platform = platform.system()
    __platform_paths = {"Linux": ".config/google-chrome", "Windows": "AppData/Local/Google/Chrome/User Data",
                        "Darwin": "Library/Application Support/Google/Chrome/"}
    # __linux_path = ".config/google-chrome"
    # __windows_path = "AppData/Local/Google/Chrome/User Data"
    # __mac_path = "Library/Application Support/Google/Chrome/"

    __profile_support = True
    __current_profile = "Default"

    __history_file = "History"
    __bookmarks_file = "Bookmarks"

    __history_sql = """
            SELECT
                datetime(
                    visits.visit_time/1000000-11644473600, 'unixepoch', 'localtime'
                ) as 'visit_time',
                urls.url,
                urls.title
            FROM
                visits INNER JOIN urls ON visits.url = urls.id
            WHERE
                visits.visit_duration > 0
            ORDER BY
                visit_time DESC
        """

    def get_bookmarks(self) -> list[tuple[str, str]]:
        try:
            with open(self.__path_to_bookmarks) as file:
                data = json.load(file)
        except Exception as e:
            raise e

        bookmarks = []
        for bookmarks_bar in data["roots"]:
            for folders in data["roots"][bookmarks_bar]["children"]:
                if folders["name"] in self.__bookmark_folders:
                    for bookmark in folders["children"]:
                        bookmarks.append((bookmark["name"], bookmark["url"]))

        return bookmarks

    def get_history(self) -> list[tuple[str, str, str]]:
        history = []
        try:

            shutil.copy(self.__path_to_history, ".")
            con = sqlite3.connect("History")
            cursor = con.cursor()
            cursor.execute(self.__history_sql)
            history = cursor.fetchall()
            os.remove("History")
        except Exception as e:
            raise e

        return history

    def _get_path_to_profile(self) -> str:
        return os.path.join(Path.home(), self.__platform_paths[self.__platform],
                            self.__current_profile)

    def _set_path(self) -> None:
        path_to_profile = self._get_path_to_profile()
        self.__path_to_history = os.path.join(path_to_profile, "History")
        self.__path_to_bookmarks = os.path.join(path_to_profile, "Bookmarks")

    def set_bookmark_folders(self, folders: list[str]) -> None:
        self.__bookmark_folders = folders

    def set_profile(self, profile: str) -> None:
        self.__current_profile = profile
        self._set_path()
