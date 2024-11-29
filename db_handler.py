import sqlite3
import logging
from itertools import chain

from requests import session
from sqlalchemy import create_engine, MetaData, ForeignKey, String, select
from sqlalchemy.orm import declarative_base, Mapped, sessionmaker, relationship
from sqlalchemy.testing.schema import mapped_column

logger = logging.getLogger(__name__)
Base = declarative_base()

class BookmarkedHistory(Base):
    __tablename__ = 'bookmarked_urls'
    url: Mapped[str] = mapped_column(primary_key = True)
    chapter: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)

    visited_urls: Mapped["VisitedHistory"] = relationship("VisitedHistory", back_populates="bookmarked_urls", cascade="all, delete-orphan")
    url_names_favicons: Mapped["UrlNamesAndFavicons"] = relationship("UrlNamesAndFavicons", back_populates="bookmarked_urls", cascade="all, delete-orphan")

    def __repr__(self):
        return f"['{self.url}', '{self.chapter}', '{self.date}']"



class VisitedHistory(Base):
    __tablename__ = 'visited_urls'
    url: Mapped[str] = mapped_column(ForeignKey("bookmarked_urls.url"), primary_key=True)
    chapter: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)

    bookmarked_urls: Mapped["BookmarkedHistory"] = relationship("BookmarkedHistory", uselist=False, back_populates="visited_urls")

    def __repr__(self):
        return f"['{self.url}', '{self.chapter}', '{self.date}']"


class UrlNamesAndFavicons(Base):
    __tablename__ = "url_names_favicons"
    url: Mapped[str] = mapped_column(ForeignKey("bookmarked_urls.url"), primary_key=True)
    url_name: Mapped[str] = mapped_column(nullable=False)
    favicon: Mapped[str] = mapped_column(nullable=False)

    bookmarked_urls: Mapped["BookmarkedHistory"] = relationship("BookmarkedHistory", uselist=False, back_populates="url_names_favicons")

    def __repr__(self):
        return f"['{self.url}', '{self.url_name}', '{self.favicon}']"


def create():
    engine = create_engine("sqlite:///data.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    bookmarked = [['https://arvencomics.com/series/0f2d5e7881d/', 'Chapter 17', '2024-11-10 18:52:10'], ['https://arvencomics.com/series/d8c9f4f52ea/', 'Chapter 7', '2024-11-10 18:52:10'], ['https://arvencomics.com/series/d11b4be7ae1/', 'Chapter 21', '2024-11-10 18:52:10'], ['https://ww8.mangakakalot.tv/manga/manga-it985502', 'Chapter 84', '2024-11-28 18:53:22'], ['https://chapmanganato.to/manga-du980903', 'Chapter 71', '2024-11-28 18:53:22'], ['https://chapmanganato.to/manga-ik985693', 'Chapter 235', '2024-11-28 18:53:22'], ['https://chapmanganato.to/manga-hu985229', 'Chapter 189.5', '2024-11-28 18:53:22'], ['https://ww8.mangakakalot.tv/manga/manga-ak977919', 'Chapter 91', '2024-11-28 18:53:22'], ['https://chapmanganato.to/manga-qi951517', 'Chapter 818', '2024-11-28 18:53:22'], ['https://ww8.mangakakalot.tv/manga/manga-ab951884', 'Chapter 523', '2024-11-28 18:53:22'], ['https://chapmanganato.to/manga-ma952557', 'Chapter 378', '2024-11-28 18:53:22'], ['https://ww8.mangakakalot.tv/manga/manga-nh991064', 'Chapter 27.2', '2024-11-28 18:53:22'], ['https://chapmanganato.to/manga-qm951521', 'Chapter 105', '2024-11-28 18:53:22'], ['https://ww8.mangakakalot.tv/manga/manga-kw988331', 'Chapter 170', '2024-11-28 18:53:22'], ['https://chapmanganato.to/manga-vz972882', 'Chapter 115', '2024-11-28 18:53:22']]
    history = [['https://arvencomics.com/series/0f2d5e7881d/', 'Chapter 17', '2024-11-10 18:52:10'], ['https://arvencomics.com/series/d8c9f4f52ea/', 'Chapter 7', '2024-11-10 18:52:10'], ['https://arvencomics.com/series/d11b4be7ae1/', 'Chapter 21', '2024-11-10 18:52:10'], ['https://ww8.mangakakalot.tv/manga/manga-nh991064', 'Chapter 0', '2024-11-28 18:48:54'], ['https://chapmanganato.to/manga-vz972882', 'Chapter 0', '2024-11-28 18:48:54'], ['https://ww8.mangakakalot.tv/manga/manga-kw988331', 'Chapter 0', '2024-11-28 18:48:54'], ['https://chapmanganato.to/manga-qi951517', 'Chapter 0', '2024-11-28 18:48:54'], ['https://chapmanganato.to/manga-hu985229', 'Chapter 0', '2024-11-28 18:48:54'], ['https://ww8.mangakakalot.tv/manga/manga-ak977919', 'Chapter 0', '2024-11-28 18:48:54'], ['https://ww8.mangakakalot.tv/manga/manga-ab951884', 'Chapter 0', '2024-11-28 18:48:54'], ['https://chapmanganato.to/manga-ma952557', 'Chapter 0', '2024-11-28 18:48:54'], ['https://chapmanganato.to/manga-du980903', 'Chapter 0', '2024-11-28 18:48:54'], ['https://chapmanganato.to/manga-ik985693', 'Chapter 235', '2024-11-28 08:11:24'], ['https://chapmanganato.to/manga-qm951521', 'Chapter 0', '2024-11-28 18:48:54'], ['https://ww8.mangakakalot.tv/manga/manga-it985502', 'Chapter 0', '2024-11-28 18:48:54']]
    favicon = [['https://arvencomics.com/series/0f2d5e7881d/', 'The Delusional Hunter in Another World', 'https://i0.wp.com/imageserver.is1.buzz//uploads/fb0e2161636?w=20'], ['https://arvencomics.com/series/d8c9f4f52ea/', 'Record of Copoka: the nine dragons', 'https://i0.wp.com/imageserver.is1.buzz//uploads/fb0e2161636?w=20'], ['https://arvencomics.com/series/d11b4be7ae1/', 'THE RAIDER', 'https://i0.wp.com/imageserver.is1.buzz//uploads/fb0e2161636?w=20'], ['https://ww8.mangakakalot.tv/manga/manga-it985502', 'Read Road To Kingdom Manga on Mangakakalot', 'https://mangakakalot.tv/static/images/favicon.ico'], ['https://chapmanganato.to/manga-du980903', 'Blue Period Manga Online Free - Manganato', 'https://chapmanganato.to/favicon.ico'], ['https://chapmanganato.to/manga-ik985693', 'Nano Machine Manga Online Free - Manganato', 'https://chapmanganato.to/favicon.ico'], ['https://chapmanganato.to/manga-hu985229', 'The Great Mage Returns After 4000 Years Manga Online Free - Manganato', 'https://chapmanganato.to/favicon.ico'], ['https://ww8.mangakakalot.tv/manga/manga-ak977919', 'Read Isekai Meikyuu De Harem O Manga on Mangakakalot', 'https://mangakakalot.tv/static/images/favicon.ico'], ['https://chapmanganato.to/manga-qi951517', 'Kingdom Manga Online Free - Manganato', 'https://chapmanganato.to/favicon.ico'], ['https://ww8.mangakakalot.tv/manga/manga-ab951884', 'Read Wind Breaker Manga on Mangakakalot', 'https://mangakakalot.tv/static/images/favicon.ico'], ['https://chapmanganato.to/manga-ma952557', 'Berserk Manga Online Free - Manganato', 'https://chapmanganato.to/favicon.ico'], ['https://ww8.mangakakalot.tv/manga/manga-nh991064', "Read An Old Man From The Countryside Becomes A Swords Saint: I Was Just A Rural Sword Teacher, But My Successful Students Won't Leave Me Alone! Manga on Mangakakalot", 'https://mangakakalot.tv/static/images/favicon.ico'], ['https://chapmanganato.to/manga-qm951521', 'Mushoku Tensei - Isekai Ittara Honki Dasu Manga Online Free - Manganato', 'https://chapmanganato.to/favicon.ico'], ['https://ww8.mangakakalot.tv/manga/manga-kw988331', "Read The Player That Can't Level Up Manga on Mangakakalot", 'https://mangakakalot.tv/static/images/favicon.ico'], ['https://chapmanganato.to/manga-vz972882', 'Blades Of The Guardians Manga Online Free - Manganato', 'https://chapmanganato.to/favicon.ico']]
    with Session.begin() as session:
        for book in bookmarked:
            session.add(BookmarkedHistory(url=book[0], chapter=book[1], date=book[2]))
        for his in history:
            session.add(VisitedHistory(url=his[0], chapter=his[1], date=his[2]))

        for fav in favicon:
            session.add(UrlNamesAndFavicons(url=fav[0], url_name=fav[1], favicon=fav[2]))


def test():
    create()
    engine = create_engine("sqlite:///data.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    with Session.begin() as session:
        # test = select(BookmarkedHistory).where(BookmarkedHistory.url=="https://chapmanganato.to/manga-qm951521")
        # print(test)
        # res = session.execute(test)
        # print(res.first())
        bookmark = session.query(VisitedHistory).where(VisitedHistory.url=="https://arvencomics.com/series/d11b4be7ae1/").first()
        print(bookmark)
        # session.delete(bookmark)
        # for book in session.query(VisitedHistory).all():
        #     print(book)


if __name__ == "__main__":
    test()



# class DbHandler:
#     __name = None
#     __db_name = "data.db"
#
#     def __init__(self, name: str):
#         self.__name = name
#         with sqlite3.connect(self.__db_name) as conn:
#             self.__connection = conn
#         self.__create_dbs()
#
#     def reset(self) -> None:
#         sql = f"drop table {self.__name}"
#         self._execute(sql)
#         self.__create_dbs()
#
#     def get_last_data(self) -> list[tuple[str, str, str]] | list[tuple[str, str]]:
#         if "chapter" in self.__name:
#             sql = f"select url, chapter, date from {self.__name}"
#         elif "url" in self.__name:
#             sql = f"select url, url_name, icon from {self.__name}"
#         else:
#             sql = f"select url, chapter, date from {self.__name}"
#         return self._execute(sql)
#
#     def get_last_time(self) -> str:
#         sql = f"select max(date) from {self.__name}"
#         # return self._execute(sql)[0][0]
#         return '2024-03-11 21:19:17'
#
#     def update(self, values: tuple[tuple[str, str, str]] | list[tuple[str, str, str]]) -> None:
#         """values: tuple(url,chapter,date)"""
#         # sql = f"update {self.__name} set date = ?, chapter = ? where url = ?"
#         # formatted_values = [(value[::-1]) for value in values]
#         # self._execute(sql, formatted_values)
#         self.create(values)
#
#     def create(self, values: list[tuple[str, str, str]]) -> None:
#         """values: tuple(url,chapter,date)"""
#         sql = f"Insert or replace into {self.__name} values(?,?,?)"
#         self._execute(sql, values)
#
#     def _execute(self, sql: str,
#                  values: [tuple[tuple[str, str, str]] | list[tuple[str, str, str]] | None] = None) \
#             -> [list[tuple[str, str]] | None]:
#
#         cur = self.__connection.cursor()
#         if ";" in sql:
#             sql = sql.split(";")
#             cur.execute(sql[0])
#             sql = sql[1]
#         if values:
#             cur.executemany(sql, values)
#         else:
#             cur.execute(sql)
#         self.__connection.commit()
#         res = cur.fetchall()
#         if sql.split()[0].lower() == "select":
#             return res
#         return None
#
#     def __create_dbs(self) -> None:
#         if "chapter" in self.__name:
#             sql_create = f"CREATE TABLE if not exists {self.__name}(url text primary key, chapter text, date date)"
#         elif "url" in self.__name:
#             sql_create = f"Create table if not exists {self.__name} (url text primary key, url_name text, icon text, foreign key (url) references last_chapters_bookmarked (url) on delete cascade)"
#         else:
#             sql_create = f"Create table if not exists {self.__name} (url text primary key, chapter text, date date, foreign key (url) references last_chapters_bookmarked (url) on delete cascade)"
#         self._execute(sql_create)
#
#
# class BookmarkedHistory(DbHandler):
#     """DB for handling history of bookmarked links
#     Fields:
#     url
#     chapter
#     date"""
#     __name = "last_chapters_bookmarked"
#
#     def __init__(self):
#         super().__init__(self.__name)
#
#     def delete_bookmarks(self, bookmarks: list[str]) -> None:
#         """
#         Params:
#         bookmarks list[str]: List of urls to delete from bookmarks"""
#         sql = f"pragma foreign_keys = ON;DELETE from {self.__name} where url = (?)"
#         self._execute(sql, bookmarks)
#
#     def get_last_data(self) -> list[tuple[str, str, str]]:
#         """Returns list of tuples(url, chapter, date)"""
#         return super().get_last_data()
#
#     def get_urls(self) -> list[str]:
#         data = self.get_last_data()
#         return [dat[0] for dat in data]
#
#
# class VisitedHistory(DbHandler):
#     """DB for handling history of visited links
#     Fields:
#     url
#     chapter
#     date"""
#     __name = "last_visited"
#
#     def __init__(self):
#         super().__init__(self.__name)
#
#     def get_last_data(self) -> list[tuple[str, str, str]]:
#         """Returns list of tuples(url, chapter, date)"""
#         return super().get_last_data()
#
#
# class UrlNamesIcons(DbHandler):
#     """Fields:
#     url
#     url_name
#     favicon_url"""
#     __name = "url_names"
#
#     def __init__(self):
#         super().__init__(self.__name)
#
#     def create(self, values: list[tuple[str, str, str]]) -> None:
#         """values: tuple(url,url_name,favicon_url)"""
#         super().create(values)
#
#     def update(self, values) -> None:
#         """values: tuple(url,url_name,favicon_url)"""
#         # sql = f"update {self.__name} set favicon_url = ?, url_name = ? where url = ?"
#         # formatted_values = [(value[::-1]) for value in values]
#         # super()._execute(sql, formatted_values)
#         self.create(values)
#
#     def get_last_data(self) -> list[tuple[str, str, str]]:
#         """Returns list of tuples(url, url_name, favicon_url)"""
#         return super().get_last_data()
#
#     def get_last_time(self) -> None:
#         raise NotImplemented
