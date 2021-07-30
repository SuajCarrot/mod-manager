# Abstract Mod class and derivates
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
# https://www.gnu.org/licenses/gpl-3.0.en.html.

import os
import shutil

import simple_logger
import global_values
import custom_exceptions

logger = simple_logger.SimpleLogger()


class Mod:
    def __init__(self, path):
        if not os.path.isfile(path):
            raise custom_exceptions.NotAFileError
        self.path = path
        self.name = os.path.basename(self.path)
        self.directory = os.path.dirname(self.path)
        self.path_when_active = os.path.join(global_values.tf2
                                             .custom_directory, self.name)
        self.backups_paths = []
        self.latest_backup_number = 0
        self.latest_backup_path = None
        logger.log(f"New Mod instance created with path {self.path}.")

    def __str__(self):
        logger.log("__str__ method called on instance of Mod.")
        return (f"Path: {self.path}\nBackups: {self.backups_paths}")

    def back_up(self):
        self.latest_backup_path = os.path.join(global_values.mod_manager
                                               .backup_directory, self.name,
                                               str(self.latest_backup_number))
        try:
            shutil.copy(self.path, self.latest_backup_path)
        except (FileExistsError, FileNotFoundError, OSError) as exception:
            exception_type = type(exception).__name__
            logger.log(f"{exception_type} exception raised when calling "
                       "back_up method on an instance of Mod.", error_level=1)
            return None
        else:
            self.backups_paths.append(self.latest_backup_path)
            self.latest_backup_number += 1
            logger.log(f"Backup of {self.path} created "
                       "({self.latest_backup_path}).")
            return self.latest_backup_path

    def remove_backup(self, backup_number):
        try:
            os.remove(self.backups_paths[backup_number])
        except IndexError:
            logger.log("Unreachable index specified on method remove_backup "
                       f"of class Mod: {backup_number}.", error_level=1)
        except (FileExistsError, OSError) as exception:
            exception_type = type(exception).__name__
            logger.log(f"{exception_type} exception raised when calling "
                       "remove_backup method on an instance of Mod.",
                       error_level=1)
        else:
            self.backups_paths[backup_number] = None
            logger.log("Backup of {self.path} removed "
                       "({self.latest_backup_path}).")

    def remove_all_backups(self):
        for backup_path in self.backups_paths:
            if backup_path is None:
                continue
            try:
                os.remove(backup_path)
            except (FileExistsError, OSError) as exception:
                exception_type = type(exception).__name__
                logger.log(f"{exception_type} exception raised on internal "
                           "iteration of remove_all_backups method of class "
                           "Mod.")
        self.backups_paths.clear()
        self.latest_backup_number = 0
        logger.log("All backups of {self.path} removed.")

    def restore_from_backup(self, backup_number):
        try:
            shutil.copy(self.backups_paths[backup_number], self.path)
        except IndexError:
            logger.log("Unreachable index specified on method "
                       f"restore_from_backup of class Mod: {backup_number}.",
                       error_level=1)
        except (FileExistsError, FileNotFoundError, OSError) as exception:
            exception_type = type(exception).__name__
            logger.log(f"{exception_type} exception raised when calling "
                       "restore_from_backup method on an instance of Mod.",
                       error_level=1)
        else:
            logger.log("{self.path} restored from backup: "
                       "{self.backups_paths[backup_number]}.")

    def restore_from_latest_backup(self):
        try:
            shutil.copy(self.latest_backup_path, self.path)
        except (FileExistsError, FileNotFoundError, OSError) as exception:
            exception_type = type(exception).__name__
            logger.log(f"{exception_type} exception raised when calling "
                       "restore_from_latest_backup method on an instance of "
                       "Mod.", error_level=1)
        else:
            logger.log("{self.path} restored from latest backup: "
                       "{self.latest_backup_path}.")


class TF2Mod(Mod):
    def activate(self):
        try:
            shutil.move(self.path, self.path_when_active)
        except (FileExistsError, FileNotFoundError, OSError) as exception:
            exception_type = type(exception).__name__
            logger.log(f"{exception_type} exception raised when calling "
                       "activate method on an instance of TF2Mod.",
                       error_level=1)
            return None
        else:
            logger.log("{self.path} moved to TF2's custom directory.")
            return self.path_when_active

    def is_active(self):
        if os.path.isfile(self.path_when_active):
            return True
        else:
            return False

    def deactivate(self):
        try:
            shutil.move(self.path, self.path_when_active)
        except (FileExistsError, FileNotFoundError, OSError) as exception:
            exception_type = type(exception).__name__
            logger.log(f"{exception_type} exception raised when calling "
                       "deactivate method on an instance of TF2Mod.",
                       error_level=1)
            return None
        else:
            logger.log("{self.name} moved to original location ({self.path}) "
                       "from TF2's custom directory.")
            return self.path

    # def add_files_from(self, target_path):
    #     for thing in os.listdir(target_path):
    #         try:
    #             if os.path.isfile(thing):
    #                 new_file_path...

    # def works_on_sv_pure_1(self):
    #     for directory in global_values.tf2.sv_pure_1_blacklisted_locations:
    #         if self.path...
