from os.path import expanduser as home
from os.path import isdir as is_dir
from os.path import join as path_join
import os


def extract_file(file_path):
    if file_path[-4:] != ".rar"\
      or file_path[-4:] != ".zip"\
      or file_path[-3:] != ".7z":
        raise CompressionFormatNotSupportedException
    else:
        os.system(f'7z x "{file_path}"')


def find_team_fortress_2_dir():
    steam_dir = "Steam/steamapps/common/Team Fortress 2/"
    for directory in (
        path_join(r"C:\Program Files (x86)", steam_dir),
        path_join(r"C:\Program Files", steam_dir),
        path_join(home("~"), ".local/share", steam_dir),
        path_join(home("~"), ".steam", steam_dir),
        path_join(home("~"), "Library/Application Support", steam_dir),
        path_join(home("~"), "Applications", steam_dir)
    ):
        if is_dir(directory):
            return directory
    else:
        raise CouldNotFindDirectoryException


def remove_cache_in_custom_dir():
    for filename in os.listdir(custom_dir):
        if filename[-6:] == ".cache":
            os.remove(path_join(custom_dir, filename))


class CouldNotFindDirectoryException(Exception):
    pass


class CompressionFormatNotSupportedException(Exception):
    pass


if __name__ == "__main__":
    custom_dir = path_join(find_team_fortress_2_dir(), "tf/custom")
