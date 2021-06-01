from os.path import isfile as is_file
from os.path import isdir as is_dir
from os.path import join as path_join
from os.path import sep as dir_sep
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
        Packs (calls the VPK CLI on a directory) the mod.
        """

        if self.is_packed():
            raise IsPackedException("The mod is already packed")
        else:
            os.system(f'"{vpk_cli_path}" "{self.path_as_dir}"')
            shutil.rmtree(self.path_as_dir)

    def unpack(self):

        """
        Unpacks (calls the VPK CLI on a VPK file) the mod.
        """

        if not self.is_packed():
            raise NotPackedException("The mod is already unpacked")
        else:
            os.system(f": $(\"{vpk_cli_path}\" \"{self.path_as_vpk}\")")
            # On UNIX, the dot in ".vpk" doesn't get removed after unpacking
            # a VPK file with the CLI that Valve provides
            if is_dir(self.path_as_dir + "."):
                os.rename(self.path_as_dir + ".", self.path_as_dir)
            os.remove(self.path_as_vpk)

    def is_active(self):

        """
        Checks if the mod is active (found in the "custom" directory).
        """

        if is_file(self.path_as_active):
            return True
        else:
            return False

    def activate(self):

        """
        Activates the mod (copies it to the "custom" directory).
        """

        if self.is_active():
            raise IsActiveException("The mod is already active")
        elif not self.is_packed():
            raise NotPackedException("The mod is not packed")
        else:
            shutil.copy(self.path_as_vpk, self.path_as_active)

    def deactivate(self):

        """
        Deactivates the mod (removes it from the "custom" directory").
        """

        if not self.is_active():
            raise NotActiveException("The mod is already inactive")
        else:
            os.remove(self.path_as_active)

    def get_internal_files(self):

        """
        Loops over the files the mod contains.
        The mod must be unpacked.
        """

        if self.is_packed():
            raise IsPackedException("Cannot get internal files from packed "
                                    "file")
        else:
            return tuple((
                files for (_, _, files_lists) in os.walk(self.path)
                for files in files_lists
            ))

    def works_in_sv_pure(self):

        # NOTE: This method is confusing compared to the other ones, improve
        # it as soon as possible. Also, create another method called
        # "get_internal_dirs".

        """
        Checks if the mod's internal files' paths are in the blacklisted
        sv_pure paths.
        """

        if self.is_packed():
            raise IsPackedException("Cannot check if the mod works in sv_pure "
                                    "while packed")
        blacklisted_dirs = (
            f"materials{dir_sep}console",
            f"materials{dir_sep}temp",
            f"materials{dir_sep}vgui{dir_sep}logos{dir_sep}ui",
            f"sound{dir_sep}misc",
            f"sound{dir_sep}vo",
            f"sound{dir_sep}ui",
        )

        mod_subdirs = tuple((
            parent for (parent, _, _) in
            os.walk(self.path_as_dir)
        ))

        for bl_dir in blacklisted_dirs:
            for mod_subdir in mod_subdirs:
                if bl_dir in mod_subdir:
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
                filename for filename in self.get_internal_files()
                if filename in other_mod.get_internal_files()
            ))
        if conflicting_files:
            return True
        else:
            return False

    def merge_with(self, other_mod):

        """
        Copies the other mod's directories to the current mod.
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
        else:
            for (parent, _, _) in os.walk(other_mod.path_as_dir):
                shutil.copytree(parent, self.path_as_dir)


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
