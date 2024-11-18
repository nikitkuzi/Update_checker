import sqlite3
import logging

logger = logging.getLogger(__name__)


class DbHandler:
    __name = None
    __db_name = "data.db"

    def __init__(self, name: str):
        self.__name = name
        with sqlite3.connect(self.__db_name) as conn:
            self.__connection = conn
        self.__create_dbs()

    def reset(self) -> None:
        sql = f"drop table {self.__name}"
        self._execute(sql)
        self.__create_dbs()

    def get_last_data(self) -> list[tuple[str, str, str]] | list[tuple[str, str]]:
        if "chapter" in self.__name:
            sql = f"select url, chapter, date from {self.__name}"
        elif "url" in self.__name:
            sql = f"select url, url_name, icon from {self.__name}"
        else:
            sql = f"select url, chapter, date from {self.__name}"
        return self._execute(sql)

    def get_last_time(self) -> str:
        sql = f"select max(date) from {self.__name}"
        # return self._execute(sql)[0][0]
        return '2024-03-11 21:19:17'

    def update(self, values: tuple[tuple[str, str, str]] | list[tuple[str, str, str]]) -> None:
        """values: tuple(url,chapter,date)"""
        # sql = f"update {self.__name} set date = ?, chapter = ? where url = ?"
        # formatted_values = [(value[::-1]) for value in values]
        # self._execute(sql, formatted_values)
        self.create(values)

    def create(self, values: list[tuple[str, str, str]]) -> None:
        """values: tuple(url,chapter,date)"""
        sql = f"Insert or replace into {self.__name} values(?,?,?)"
        self._execute(sql, values)

    def _execute(self, sql: str,
                 values: [tuple[tuple[str, str, str]] | list[tuple[str, str, str]] | None] = None) \
            -> [list[tuple[str, str]] | None]:

        cur = self.__connection.cursor()
        if ";" in sql:
            sql = sql.split(";")
            cur.execute(sql[0])
            sql = sql[1]
        if values:
            cur.executemany(sql, values)
        else:
            cur.execute(sql)
        self.__connection.commit()
        res = cur.fetchall()
        if sql.split()[0].lower() == "select":
            return res
        return None

    def __create_dbs(self) -> None:
        if "chapter" in self.__name:
            sql_create = f"CREATE TABLE if not exists {self.__name}(url text primary key, chapter text, date date)"
        elif "url" in self.__name:
            sql_create = f"Create table if not exists {self.__name} (url text primary key, url_name text, icon text, foreign key (url) references last_chapters_bookmarked (url) on delete cascade)"
        else:
            sql_create = f"Create table if not exists {self.__name} (url text primary key, chapter text, date date, foreign key (url) references last_chapters_bookmarked (url) on delete cascade)"
        self._execute(sql_create)


class BookmarkedHistory(DbHandler):
    """DB for handling history of bookmarked links
    Fields:
    url
    chapter
    date"""
    __name = "last_chapters_bookmarked"

    def __init__(self):
        super().__init__(self.__name)

    def delete_bookmarks(self, bookmarks: list[str]) -> None:
        """
        Params:
        bookmarks list[str]: List of urls to delete from bookmarks"""
        sql = f"pragma foreign_keys = ON;DELETE from {self.__name} where url = (?)"
        self._execute(sql, bookmarks)

    def get_last_data(self) -> list[tuple[str, str, str]]:
        """Returns list of tuples(url, chapter, date)"""
        return super().get_last_data()

    def get_urls(self) -> list[str]:
        data = self.get_last_data()
        return [dat[0] for dat in data]


class VisitedHistory(DbHandler):
    """DB for handling history of visited links
    Fields:
    url
    chapter
    date"""
    __name = "last_visited"

    def __init__(self):
        super().__init__(self.__name)

    def get_last_data(self) -> list[tuple[str, str, str]]:
        """Returns list of tuples(url, chapter, date)"""
        return super().get_last_data()


class UrlNamesIcons(DbHandler):
    """Fields:
    url
    url_name
    favicon_url"""
    __name = "url_names"

    def __init__(self):
        super().__init__(self.__name)

    def create(self, values: list[tuple[str, str, str]]) -> None:
        """values: tuple(url,url_name,favicon_url)"""
        super().create(values)

    def update(self, values) -> None:
        """values: tuple(url,url_name,favicon_url)"""
        # sql = f"update {self.__name} set favicon_url = ?, url_name = ? where url = ?"
        # formatted_values = [(value[::-1]) for value in values]
        # super()._execute(sql, formatted_values)
        self.create(values)

    def get_last_data(self) -> list[tuple[str, str, str]]:
        """Returns list of tuples(url, url_name, favicon_url)"""
        return super().get_last_data()

    def get_last_time(self) -> None:
        raise NotImplemented
