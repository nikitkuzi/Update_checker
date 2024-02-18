import platform


class LoadDir:
    def __init__(self, dir: str, profiles: list[str]):
        self.platform = platform.system()
        self.dir = dir
        self.profiles = profiles

    def get_path(self):
        pass