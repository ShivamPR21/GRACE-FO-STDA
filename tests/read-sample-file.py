#!/usr/bin/env python3
#
# GRACE-FO-STDA
# Copyright (C) 2020  Shivam Pandey pandeyshivam2017robotics@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

from grace_fo_stda.grace_read.read import read


def read_sample_file():
    """
        Load and verify the GRACE and GRACE-FO sample data.
    """
    files_path = [os.getcwd() + "/../Data/" + x for x in os.listdir("../Data/")]

    try:
        data = read(files_path)
        return True
    except ValueError:
        raise ValueError("The read function has some bug please report it for further actions.")


if __name__ == "__main__":
    print(read_sample_file())
