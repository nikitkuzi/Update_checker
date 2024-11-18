from browsers import Chrome
from web_handler import WebHandler
from db_handler import BookmarkedHistory, VisitedHistory, UrlNamesIcons
import logging
from web_handler import ChapterInfo



def strip_urls(urls):
    stripped_urls = []
    for url in urls:
        splitted = url.split("/")
        if splitted[2][0] == 'w' and splitted[2][1] == 'w':
            pos = splitted[2].find('.')
            stripped_urls.append(splitted[2][pos + 1:])
        else:
            stripped_urls.append(splitted[2])
    return stripped_urls


def update_dbs(data: list[ChapterInfo], bookmark_db: BookmarkedHistory, history_db: VisitedHistory,
               url_names_db: UrlNamesIcons) -> None:
    bookmarked_data = [(bookmark.url, bookmark.chapter, bookmark.time) for bookmark in data]
    bookmarked_names_and_icons = [(bookmark.url, bookmark.url_name, bookmark.favicon_url) for bookmark in data]

    bookmark_db.create(bookmarked_data)
    history_db.create(bookmarked_data)
    url_names_db.create(bookmarked_names_and_icons)
    logger.info(f"Updated Dbs")


if __name__ == '__main__':
    # config
    folders = ['manga11', 'manga', 'manga1', 'manga2', 'manga3', 'manga4', 'manga5', 'manga6', 'manga7']
    logger = logging
    logger.basicConfig(filename='log.log', level=logging.DEBUG,
                       format='%(levelname)s: %(name)s - %(asctime)s - %(message)s', datefmt='%d/%b/%y %H:%M:%S')
    # get history and bookmarks from Chrome
    browser = Chrome()
    browser.set_bookmark_folders(folders)
    bookmarks = browser.get_bookmarks()
    history = browser.get_history()

    # parse url and get data from it
    parser = WebHandler()
    bookmarked_urls = [bookmark[0] for bookmark in bookmarks]
    supported_urls = parser.get_supported_urls(bookmarked_urls)
    data = parser.get_bookmarked_data(supported_urls)
    # print(Counter(strip_urls(bookmarked_urls)))
    # exit(0)

    bookmark_db = BookmarkedHistory()
    history_db = VisitedHistory()
    url_names_db = UrlNamesIcons()

    # update if there are new bookmarks
    update_dbs(data, bookmark_db, history_db, url_names_db)

    # update supported url to deal with redirections
    # when bookmarked url is not an actual url
    supported_urls = parser.get_supported_urls(bookmark_db.get_urls())

    # get latest chapters read
    # and update history db
    last_visited_chapters = parser.get_last_visited_supported_chapters_from_history(supported_urls, history, history_db.get_last_time())
    history_db.update(last_visited_chapters)
    print(last_visited_chapters)

    # get latest chapter if you havent read it
    to_read = parser.get_diff(bookmark_db.get_last_data(), history_db.get_last_data(), url_names_db.get_last_data())
    print(to_read)
