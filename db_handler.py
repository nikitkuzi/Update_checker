import sqlite3
import os


class DbHandler:
    __last_chapters_bookmarked = "last_chapters_bookmarked"
    __last_visited = "last_visited"

    def __init__(self):
        self.__create_dbs()

    def update_last_chapters_bookmarked(self, values: [tuple[tuple[str, str]] | list[tuple[str, str]]]):
        """Updates db of last chapters from bookmarked urls.
        values: tuple(chapter,url)"""
        sql = "update last_chapters_bookmarked set chapter = ? where url = ?"
        self.__execute_last_chapters_bookmarked(sql, values)
        # with sqlite3.connect(self.__last_chapters_bookmarked) as conn:
        #     cur = conn.cursor()
        #     cur.executemany(sql, values)
        #     conn.commit()
        #     print(self.__get_db(self.__last_chapters_bookmarked))

    def create_last_chapters_bookmarked(self, values: [tuple[tuple[str, str]] | list[tuple[str, str]]]):
        sql = "Insert into last_chapters_bookmarked(chapter, url) values(?,?)"
        self.__execute_last_chapters_bookmarked(sql, values)
        # with sqlite3.connect(self.__last_chapters_bookmarked) as conn:
        #     cur = conn.cursor()
        #     cur.executemany(sql, values)
        #     conn.commit()
        #     print(self.__get_db(self.__last_chapters_bookmarked))

    def get_last_chapters_bookmarked(self):
        sql = "select * from last_chapters_bookmarked"
        return self.__execute_last_chapters_bookmarked(sql)
        # with sqlite3.connect(self.__last_chapters_bookmarked) as conn:
        #     cur = conn.cursor()
        #     cur.execute(sql)
        #     return cur.fetchall()

    def reset_last_chapters_bookmarked(self):
        sql = "drop table last_chapters_bookmarked"
        self.__execute_last_chapters_bookmarked(sql)
        self.__create_dbs()

    def __execute_last_chapters_bookmarked(self, sql: str,
                                           values: [tuple[tuple[str, str]] | list[tuple[str, str]]] = None) -> \
            [
                list[str] | None]:
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

    def __get_db(self, name: str) -> list[str]:
        get = f"select * from {name}"
        with sqlite3.connect(name) as conn:
            cur = conn.cursor()
            cur.execute(get)
            return cur.fetchall()

    def __create_dbs(self):
        if not os.path.exists(self.__last_chapters_bookmarked):
            sql_create = "CREATE TABLE last_chapters_bookmarked(url text primary key, chapter text);"
            with sqlite3.connect(self.__last_chapters_bookmarked) as conn:
                conn.executescript(sql_create)
        if not os.path.exists(self.__last_visited):
            sql_create = "CREATE TABLE last_visited(url text primary key, date_visited date)"
            with sqlite3.connect(self.__last_visited) as conn:
                conn.executescript(sql_create)
