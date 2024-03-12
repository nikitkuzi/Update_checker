import abc
import sqlite3
import os


class DbHandler:
    __name = None
    __db_name = "data.db"

    def __init__(self, name: str):
        self.__name = name
        self.__create_dbs()

    def reset(self):
        sql = f"drop table {self.__name}"
        self._execute(sql)
        self.__create_dbs()

    def get_last_data(self) -> list[tuple[str, str]]:
        if "chapter" in self.__name:
            sql = f"select url, chapter from {self.__name}"
        else:
            sql = f"select url, chapter, date from {self.__name}"
        return self._execute(sql)

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

    def __create_dbs(self):
        if "chapter" in self.__name:
            sql_create = f"CREATE TABLE if not exists {self.__name}(url text primary key, chapter text)"
        else:
            sql_create = f"Create table if not exists {self.__name} (url text primary key, chapter text, date date, foreign key (url) references last_chapters_bookmarked (url) on delete cascade)"
        with sqlite3.connect(self.__db_name) as conn:
            conn.execute(sql_create)
            conn.commit()


class BookmarkedHistory(DbHandler):
    __name = "last_chapters_bookmarked"

    def __init__(self):
        super().__init__(self.__name)

    def update(self, values: [tuple[tuple[str, str]] | list[tuple[str, str]]]):
        """Updates db of last chapters from bookmarked urls.
        values: tuple(chapter,url)"""
        sql = f"update {self.__name} set chapter = ? where url = ?"
        self._execute(sql, values)

    def delete_bookmarks(self, bookmarks: list[tuple[str, str]]):
        values = [(bookmark[0],) for bookmark in bookmarks]
        sql = f"pragma foreign_keys = ON;DELETE from {self.__name} where url = (?)"
        self._execute(sql, values)

    def create(self, values: [tuple[tuple[str, str]] | list[tuple[str, str]]]):
        sql = f"Insert or ignore into {self.__name} values(?,?)"
        self._execute(sql, values)


class VisitedHistory(DbHandler):
    __name = "last_visited"

    def __init__(self):
        super().__init__(self.__name)

    def update(self, values: [tuple[tuple[str, str]] | list[tuple[str, str]]]):
        """Updates db of last visited urls from bookmarked urls.
        values: tuple(date,chapter,url)"""
        sql = f"update {self.__name} set date = ?, chapter = ? where url = ?"
        self._execute(sql, values)

    def get_last_time(self) -> str:
        sql = f"select max(date) from {self.__name}"
        return self._execute(sql)[0][0]

    def create(self, values: [tuple[tuple[str, str]] | list[tuple[str, str]]]):
        sql = f"Insert or ignore into {self.__name} values(?,?,?)"
        self._execute(sql, values)
