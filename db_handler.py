import sqlite3
import os

class DbHandler:
    __last_chapters_bookmarked = "last_chapters_bookmarked"
    __last_visited = "last_visited"
    def __init__(self):
        if not os.path.exists(self.__last_chapters_bookmarked):
            sql_create = "CREATE TABLE last_chapters_bookmarked(url text primary key, chapter text);"
            with sqlite3.connect(self.__last_chapters_bookmarked) as conn:
                conn.executescript(sql_create)
        if not os.path.exists(self.__last_visited):
            sql_create = "CREATE TABLE last_visited(url text primary key, date_visited date)"
            with sqlite3.connect(self.__last_visited) as conn:
                conn.executescript(sql_create)


    def update_last_chapters_bookmarked(self, values):
        sql = "Insert into last_chapters_bookmarked(name, chapter) values(?,?) on duplicate"
        with sqlite3.connect(self.__last_chapters_bookmarked) as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
