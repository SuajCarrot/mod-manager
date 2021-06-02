# The module that defines the "Mod" class
#
# Copyright (C) 2021  Suaj
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# https://www.gnu.org/licenses/gpl-3.0.en.html

from os.path import isfile as is_file
from os.path import isdir as is_dir
from os.path import join as path_join
import shutil
import os


class Mod:
    def __init__(self, filename):

        """
        Mod class constructor, defines possible paths from the given filename.
        The mod (file or directory) must be located at the database directory.
        """

        self.filename = filename
        self.path_as_vpk = path_join(db_dir, self.filename + ".vpk")
        self.path_as_dir = path_join(db_dir, self.filename)
        self.path_as_active = path_join(custom_dir, self.filename + ".vpk")

    def reset_filename(self, filename):

        """
        Redefines possible paths from the given filename.
        Renames the mod (file or directory) if it exists using the new paths.
        """

        self.filename = filename
        new_path_as_vpk = path_join(db_dir, self.filename + ".vpk")
        new_path_as_dir = path_join(db_dir, self.filename)

        if self.is_packed():
            os.rename(self.path_as_vpk, new_path_as_vpk)
        elif not self.is_packed():
            os.rename(self.path_as_dir, new_path_as_dir)
        else:
            pass

        self.path_as_vpk = new_path_as_vpk
        self.path_as_dir = new_path_as_dir

    def is_packed(self):

        """
        Checks if the mod is packed (a VPK file) or not.
        """

        if is_file(self.path_as_vpk):
            return True
        else:
            return False

    def pack(self):

        """
        Calls the VPK CLI on a directory (the mod).
        """

        if self.is_packed():
            raise IsPackedException("The mod is already packed")
        else:
            os.system(f'"{vpk_cli_path}" "{self.path_as_dir}"')
            shutil.rmtree(self.path_as_dir)

    def unpack(self):

        """
        Calls the VPK CLI on a VPK file (the mod).
        """

        if not self.is_packed():
            raise NotPackedException("The mod is already unpacked")
        else:
            os.system(f'"{vpk_cli_path}" "{self.path_as_vpk}"')
            # On UNIX, the dot in ".vpk" doesn't get removed after unpacking
            # a VPK file with the CLI that Valve provides
            if is_dir(self.path_as_dir + "."):
                os.rename(self.path_as_dir + ".", self.path_as_dir)
            os.remove(self.path_as_vpk)

    def is_active(self):

        """
        Checks if the mod is in the game's "custom" directory.
        """

        if is_file(self.path_as_active):
            return True
        else:
            return False

    def activate(self):

        """
        Copies the mod to the game's "custom" directory.
        """

        if self.is_active():
            raise IsActiveException("The mod is already active")
        elif not self.is_packed():
            raise NotPackedException("The mod is not packed")
        else:
            shutil.copy(self.path_as_vpk, self.path_as_active)

    def deactivate(self):

        """
        Removes the mod from the game's "custom" directory.
        """

        if not self.is_active():
            raise NotActiveException("The mod is already inactive")
        else:
            os.remove(self.path_as_active)

    def get_own_files_with_relative_paths(self):

        """
        Loops over the files the mod contains with their relative paths.
        The mod must be unpacked.
        """

        if self.is_packed():
            raise IsPackedException("Cannot get internal files from packed "
                                    "file")
        else:
            return tuple((
                path_join(parent.strip(self.path_as_dir), internal_file)
                for (parent, _, files_lists) in os.walk(self.path_as_dir)
                for internal_file in files_lists
            ))

    def works_in_sv_pure(self):

        """
        Checks if the sv_pure blacklisted paths are somewhere in the mod's
        internal files' paths.
        """

        if self.is_packed():
            raise IsPackedException("Cannot check if the mod works in sv_pure "
                                    "while packed")

        for file_path in self.get_own_files_with_relative_paths():
            if path_join("materials", "console") in file_path\
              or path_join("materials", "temp") in file_path\
              or path_join("materials", "vgui", "logos", "ui") in file_path\
              or path_join("sound", "misc") in file_path\
              or path_join("sound", "vo") in file_path\
              or path_join("sound", "ui") in file_path:
                return False
        else:
            return True

    def conflicts_with(self, other_mod):

        """
        Checks if the mod shares one or more internal file with the other mod.
        Both mods must be unpacked.
        """

        if not isinstance(other_mod, Mod):
            raise NotAModException("The specified mod is not registered in "
                                   "the database")
        elif self.is_packed() or other_mod.is_packed():
            raise IsPackedException("One or both mods are packed")
        else:
            conflicting_files = tuple((
                file_path
                for file_path in self.get_own_files_with_relative_paths()
                if file_path in other_mod.get_own_files_with_relative_paths()
            ))
        if conflicting_files:
            return True
        else:
            return False

    def merge_with(self, other_mod):

        """
        Copies the other mod's directories (trees) to the current mod.
        Both mods must be unpacked.
        """

        if not isinstance(other_mod, Mod):
            raise NotAModException("The specified mod is not registered in "
                                   "the database")
        elif self.is_packed() or other_mod.is_packed():
            raise IsPackedException("One or both mods are packed")
        elif self.conflicts_with(other_mod):
            raise ConflictsWithModException("The mods share one or more "
                                            "files")
        for tree in tuple((
            name for name in os.listdir(other_mod.path_as_dir)
            if is_dir(path_join(other_mod.path_as_dir, name))
        )):
            shutil.copytree(
                path_join(other_mod.path_as_dir, tree),
                path_join(self.path_as_dir, tree)
            )


class IsPackedException(Exception):
    pass


class NotPackedException(Exception):
    pass


class IsActiveException(Exception):
    pass


class NotActiveException(Exception):
    pass


class NotAModException(Exception):
    pass


class ConflictsWithModException(Exception):
    pass


if __name__ == "__main__":
    import misc

    # The database can be whatever directory you want
    custom_dir = path_join(misc.find_team_fortress_2_dir(), "/tf/custom/")
    vpk_cli_path = path_join(misc.find_team_fortress_2_dir(), "/bin/vpk")
    db_dir = "/home/suaj/Programs/TF2MTK/src/database/"
