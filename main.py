import os
import json
def loadUserBookmarks():
    """Load user bookmarks"""
    p = os.path.normpath(r"Google\Chrome\User Data\Default\Bookmarks")
    path = os.getenv('LOCALAPPDATA')

    with open(os.path.join(path, p), encoding='utf-8') as file:
       print(json.load(file))

if __name__ == '__main__':
    loadUserBookmarks()


