import os
import json


def load_user_bookmarks():
    """Load user bookmarks"""

    with open(get_path("Bookmarks"), encoding='utf-8') as file:
        data = json.load(file)

    folders = {'manga', 'manga1', 'manga2', 'manga3'}
    urls = []
    for folder in data['roots']['bookmark_bar']['children']:
        if folder['name'] in folders:
            for bookmark in folder['children']:
                urls.append(bookmark['url'])
    print(len(urls))
    print(urls)


def get_path(filename: str):
    return os.path.join(os.getenv('LOCALAPPDATA'), r"Google\Chrome\User Data\Default", filename)


if __name__ == '__main__':
    load_user_bookmarks()


