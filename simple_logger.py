# A simple logger, the standard logging module is not used instead because it's
# quite messy
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
from datetime import datetime

import global_values


class SimpleLogger:
    def __init__(self, file_name="mod-manager-log.txt"):
        self.file_name = file_name
        self.path = os.path.join(global_values.mod_manager.log_directory,
                                 file_name)

    def write_header(self):
        with open(self.path, "a") as log_file:
            log_file.write("Log file created by the Mod Manager on {}.\n\n"
                           .format(datetime.now().strftime("%b %d, %Y")))

    def write_date_separator(self):
        with open(self.path, "a") as log_file:
            log_file.write("----------{}----------\n".format(datetime.now()
                           .strftime("%B %d, %Y")).upper())

    def log(self, message, error_level=0):
        if error_level == 0:
            error_level = "INFO"
        elif error_level == 1:
            error_level = "ERROR"
        elif error_level == 2:
            error_level = "CRITICAL ERROR"

        with open(self.path, "a") as log_file:
            log_file.write("{}>{}-{}: {}\n".format(__name__, datetime.now()
                           .strftime("%H:%M:%S"), error_level, message))
