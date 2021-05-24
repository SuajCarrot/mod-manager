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
    def __init__(self, filename):
        if filename[-4:] != ".vpk":
            raise NotAVPKException
        else:
            self.filename = filename
        self.path = path_join(db_dir, self.filename)

    def set_filename(self, filename):
        if self.is_active():
            raise IsActiveException
        if not self.is_packed():
            raise IsPackedException
        if filename[-4:] != ".vpk":
            raise NotAVPKException
        else:
            self.filename = filename
            new_path = path_join(db_dir, self.filename)
            os.rename(self.path, new_path)
            self.path = new_path

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

        if is_dir(self.path[:-4]):  # "file.vpk" -> "file"
            self.path = self.path[:-4]

        elif is_dir(self.path[:-3]):  # "file.vpk" -> "file."
            os.rename(self.path[:-3], self.path[:-4])  # "file." -> "file"
            self.path = self.path[:-4]
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
        if not self.is_active():
            raise NotActiveException
        else:
            os.remove(path_join(custom_dir, self.filename))

    def is_active(self):
        if is_file(path_join(custom_dir, self.filename)):
            return True
        else:
            return False

    def get_internal_files(self):
        if self.is_packed():
            raise IsPackedException
        if self.is_active():
            raise IsActiveException
        else:
            internal_files = tuple((
                files
                for (_, _, files_lists) in os.walk(self.path)
                for files in files_lists
            ))
        return internal_files

    def conflicts_with(self, other_mod):
        if not isinstance(other_mod, Mod):
            raise NotAModException
        else:
            conflicting_files = tuple((
                filename for filename in self.get_internal_files()
                if filename in other_mod.get_internal_files()
            ))
        if conflicting_files:
            return True
        else:
            return False

    def merge_with(self, other_mod):
        if not isinstance(other_mod, Mod):
            raise NotAModException
        if self.is_packed() or other_mod.is_packed():
            raise IsPackedException
        if self.conflicts_with(other_mod):
            raise ConflictsWithModException
        else:
            dirs_to_copy = (
                directory
                for (directory, _, _) in os.walk(other_mod.path)
            )
            for directory in dirs_to_copy:
                shutil.copytree(directory, self.path)

        # After being merged, it should conflict with the other mod
        if not self.conflicts_with(other_mod):
            raise CouldNotMergeException


class NotAVPKException(Exception):
    pass


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


class NotAModException(Exception):
    pass


class ConflictsWithModException(Exception):
    pass


class CouldNotMergeException(Exception):
    pass
