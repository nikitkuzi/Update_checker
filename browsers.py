import abc
import json
import os
import shutil
import sqlite3
from pathlib import Path
import platform


class Browser(abc.ABC):
    __platform_paths: dict[str, [str | None]]
    """Dictionary containing default paths of supported platforms"""

    __profile_support: bool
    """Boolean indicating whether the browser supports multiple profiles."""

    __current_profile: [str | None]
    """List of possible prefixes for the profile directories."""

    __bookmarks_file: str
    """Name of the JSON file which stores the bookmarks."""

    __history_file: str
    """Name of the SQLite file which stores the history."""

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
        supported = ("Windows", "Linux", "Darwin")
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

    __current_platform = platform.system()
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
                urls.url,
                datetime(
                    visits.visit_time/1000000-11644473600, 'unixepoch', 'localtime'
                ) as 'visit_time',
                urls.title
            FROM
                visits INNER JOIN urls ON visits.url = urls.id
            ORDER BY
                visit_time DESC
            LIMIT 5000
        """
    """Sql query for fetching history data"""

    def get_bookmarks(self) -> list[tuple[str, str]]:
        """Returns list of all bookmarks in selected folders"""
        try:
            with open(self.__path_to_bookmarks, encoding="utf-8") as file:
                data = json.load(file)
        except Exception as e:
            raise e

        bookmarks = []
        for bookmarks_bar in data["roots"]:
            for folders in data["roots"][bookmarks_bar]["children"]:
                if folders["name"] in self.__bookmark_folders:
                    for bookmark in folders["children"]:
                        bookmarks.append((bookmark["url"], bookmark["name"]))

        return bookmarks

    def get_history(self) -> list[tuple[str, str, str]]:
        """Returns readable chrome history of last 5000 visits"""
        history = []
        try:
            shutil.copy(self.__path_to_history, ".")
            con = sqlite3.connect("History")
            cursor = con.cursor()
            cursor.execute(self.__history_sql)
            history = cursor.fetchall()
            con.close()
            os.remove("History")
        except Exception as e:
            raise e

        return history

    def _get_path_to_profile(self) -> str:
        return os.path.join(Path.home(), self.__platform_paths[self.__current_platform],
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
