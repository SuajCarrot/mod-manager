from urllib.request import urlretrieve as download_from_url
from os.path import isfile as is_file
from os.path import isdir as is_dir
from os.path import join as path_join
import shutil
import os

custom_dir = ("/home/suaj/.local/share/Steam/steamapps/common/Team Fortress "
              "2/tf/custom/")
vpk_cli = ("/home/suaj/.local/share/Steam/steamapps/common/Team Fortress "
           "2/bin/vpk")
db_dir = "/home/suaj/Programs/TF2MTK/src/database/"


class Mod:
    def __init__(self, filename, dl_url=None):
        self.filename = filename
        self.dl_url = dl_url
        self.path = path_join(db_dir, self.filename)

    def download(self):
        if self.dl_url is None:
            raise DownloadURLNotProvidedException
        if self.is_downloaded():
            raise AlreadyDownloadedException
        else:
            download_from_url(self.dl_url, self.path)

    def delete(self):
        if self.is_active():
            raise IsActiveException
        if not self.is_downloaded():
            raise NotDownloadedException
        else:
            os.remove(self.path)
        self.path = ""

    def is_downloaded(self):
        if is_dir(self.path) or is_file(self.path):
            return True
        else:
            return False

    def pack(self):
        if self.is_packed():
            raise IsPackedException
        else:
            # ": $(command)" to stop output to the screen
            os.system(f": $(\"{vpk_cli}\" \"{self.path}\")")
            shutil.rmtree(self.path)

            self.path += ".vpk"
            if not is_file(self.path):
                raise CouldNotPackException

    def unpack(self):
        if self.is_active():
            raise IsActiveException
        if not self.is_packed():
            raise NotPackedException
        else:
            os.system(f": $(\"{vpk_cli}\" \"{self.path}\")")
            os.remove(self.path)

            # On UNIX, the dot in ".vpk" doesn't get removed after unpacking
            # a VPK file with the CLI that Valve provides

            for name in os.listdir(db_dir):
                if name in self.filename[:-3]:  # Last 3 chars are "vpk"
                    self.path = path_join(db_dir, name)
                    os.rename(self.path, self.path[:-1])  # Remove the dot
                    self.path = self.path[:-1]
                    break
            else:
                raise CouldNotUnpackException

    def is_packed(self):
        if self.path[-4:] == ".vpk":
            return True
        else:
            return False

    def activate(self):
        if self.is_active():
            raise IsActiveException
        if not self.is_packed():
            raise NotPackedException
        else:
            shutil.copy(self.path, path_join(custom_dir, self.filename))

    def deactivate(self):
        if self.is_active():
            os.remove(path_join(custom_dir, self.filename))
        else:
            raise NotActiveException

    def is_active(self):
        if is_file(path_join(custom_dir, self.filename)):
            return True
        else:
            return False

    def get_internal_files(self):
        if self.is_packed():
            raise IsPackedException
        else:
            internal_files = tuple((
                path_join(parent, single_file)
                for (parent, dirs, files) in os.walk(self.path)
                for single_file in files
            ))
        return internal_files


class DownloadURLNotProvidedException(Exception):
    pass


class AlreadyDownloadedException(Exception):
    pass


class NotDownloadedException(Exception):
    pass


class IsPackedException(Exception):
    pass


class NotPackedException(Exception):
    pass


class IsActiveException(Exception):
    pass


class NotActiveException(Exception):
    pass


class CouldNotPackException(Exception):
    pass


class CouldNotUnpackException(Exception):
    pass
