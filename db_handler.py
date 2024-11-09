import abc
import sqlite3
import os


class DbHandler:
    __name = None
    __db_name = "data.db"

    def __init__(self, name: str):
        self.__name = name
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

    def update(self, values: [tuple[tuple[str, str, str]] | list[tuple[str, str, str]]]) -> None:
        """values: tuple(url,chapter,date)"""
        sql = f"update {self.__name} set date = ?, chapter = ? where url = ?"
        formatted_values = [(value[::-1]) for value in values]
        self._execute(sql, formatted_values)

    def create(self, values: list[tuple[str, str, str]]) -> None:
        sql = f"Insert or ignore into {self.__name} values(?,?,?)"
        self._execute(sql, values)

    def _execute(self, sql: str,
                 values: [tuple[tuple[str, str]] | list[tuple[str, str]] | None] = None) \
            -> [list[tuple[str, str]] | None]:
        with sqlite3.connect(self.__db_name) as conn:
            cur = conn.cursor()
            if ";" in sql:
                sql = sql.split(";")
                cur.execute(sql[0])
                sql = sql[1]
            if values:
                cur.executemany(sql, values)
            else:
                cur.execute(sql)
            conn.commit()
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
        sql = f"pragma foreign_keys = ON;DELETE from {self.__name} where url = (?)"
        self._execute(sql, bookmarks)


class VisitedHistory(DbHandler):
    """DB for handling history of visited links
    Fields:
    url
    chapter
    date"""
    __name = "last_visited"

    def __init__(self):
        super().__init__(self.__name)


class UrlNamesIcons(DbHandler):
    """Fields:
    url
    url_name
    icon_url"""
    __name = "url_names"

    def __init__(self):
        super().__init__(self.__name)

    def update(self) -> None:
        pass

    def get_last_time(self) -> None:
        pass
