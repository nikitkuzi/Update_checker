import abc
import sqlite3
import os


class DbHandler(abc.ABC):

    @abc.abstractmethod
    def update(self, values: [tuple[tuple[str, str]] | list[tuple[str, str]]]) -> None:
        pass

    @abc.abstractmethod
    def create(self, values: [tuple[tuple[str, str]] | list[tuple[str, str]]]) -> None:
        pass

    @abc.abstractmethod
    def reset(self) -> None:
        pass

    @abc.abstractmethod
    def _execute(self, sql: str,
                 values: [tuple[tuple[str, str]] | list[tuple[str, str]] | None] = None) \
            -> [list[str] | None]:
        pass


class Bookmarked(DbHandler):
    __last_chapters_bookmarked = "last_chapters_bookmarked"

    def __init__(self):
        self.__create_dbs()

    def update(self, values: [tuple[tuple[str, str]] | list[tuple[str, str]]]):
        """Updates db of last chapters from bookmarked urls.
        values: tuple(chapter,url)"""
        sql = "update last_chapters_bookmarked set chapter = ? where url = ?"
        self._execute(sql, values)

    def create(self, values: [tuple[tuple[str, str]] | list[tuple[str, str]]]):
        sql = "Insert or ignore into last_chapters_bookmarked(chapter, url) values(?,?)"
        self._execute(sql, values)

    def get_last_chapters(self):
        sql = "select * from last_chapters_bookmarked"
        return self._execute(sql)

    def reset(self):
        os.remove(self.__last_chapters_bookmarked)
        self.__create_dbs()

    def _execute(self, sql: str,
                 values: [tuple[tuple[str, str]] | list[tuple[str, str]] | None] = None) \
            -> [list[str] | None]:
        with sqlite3.connect(self.__last_chapters_bookmarked) as conn:
            cur = conn.cursor()
            if values:
                cur.executemany(sql, values)
            else:
                cur.execute(sql)
            conn.commit()
            if sql.split()[0].lower() == "select":
                return cur.fetchall()
            return None

    def __create_dbs(self):
        if not os.path.exists(self.__last_chapters_bookmarked):
            sql_create = "CREATE TABLE last_chapters_bookmarked(url text primary key, chapter text);"
            with sqlite3.connect(self.__last_chapters_bookmarked) as conn:
                conn.executescript(sql_create)
                conn.commit()

    def __get_db(self, name: str) -> list[str]:
        get = f"select * from {name}"
        with sqlite3.connect(name) as conn:
            cur = conn.cursor()
            cur.execute(get)
            return cur.fetchall()
