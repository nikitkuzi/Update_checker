import abc
import sqlite3
import os


class DbHandler:
    __name = None

    def __init__(self, name: str):
        self.__name = name
        self.__create_dbs()

    def create(self, values: [tuple[tuple[str, str]] | list[tuple[str, str]]]):
        sql = f"Insert or ignore into {self.__name} values(?,?)"
        self._execute(sql, values)

    def reset(self):
        os.remove(self.__name)
        self.__create_dbs()

    def get_last_data(self):
        if "chapter" in self.__name:
            sql = f"select chapter, url from {self.__name}"
        else:
            sql = f"select date, url from {self.__name}"
        return self._execute(sql)

    def _execute(self, sql: str,
                 values: [tuple[tuple[str, str]] | list[tuple[str, str]] | None] = None) \
            -> [list[str] | None]:
        with sqlite3.connect(self.__name) as conn:
            cur = conn.cursor()
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
        if not os.path.exists(self.__name):
            if "chapter" in self.__name:
                sql_create = f"CREATE TABLE {self.__name}(url text primary key, chapter text);"
            else:
                sql_create = f"Create table {self.__name} (url text primary key, date date);"
            with sqlite3.connect(self.__name) as conn:
                conn.executescript(sql_create)
                conn.commit()


class Bookmarked(DbHandler):
    __name = "last_chapters_bookmarked"

    def __init__(self):
        super().__init__(self.__name)

    def update(self, values: [tuple[tuple[str, str]] | list[tuple[str, str]]]):
        """Updates db of last chapters from bookmarked urls.
        values: tuple(chapter,url)"""
        sql = f"update {self.__name} set chapter = ? where url = ?"
        self._execute(sql, values)


class History(DbHandler):
    __name = "last_visited"

    def __init__(self):
        super().__init__(self.__name)

    def get_last_time(self):
        sql = f"select max(date) from {self.__name}"
        return self._execute(sql)
