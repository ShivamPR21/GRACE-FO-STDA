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

"""
Header information retrieval for further data processing and directly reading useful information of Spherical Harmonic
Coefficients.
"""

import re
from datetime import datetime
import numpy as np


def parse_datetime(str_):
    """

    :param str_:
    """
    str_info = list(filter(None, re.split(": |T| ", str_)))
    date_ = datetime.strptime(str_info[1].strip(), "%Y-%m-%d").date()
    for time_fmt in ["%H:%M:%S.%f", "%H:%M:%S", "%H.%M.%S.%f"]:
        try:
            time_ = datetime.strptime(str_info[2].strip(), time_fmt).time()
            return date_, time_
        except ValueError:
            pass

    raise ValueError("The format of time %s is not supported", str_info[2].strip())


def read_header(files):
    """
    Function reads all the file names provided and returns header info list.
    :param files: Path to files as list of strings.
    :return: Header list containing information about start and end date for
    each data file, heading information, and lines to skip
    """

    header_list = []
    for file in files:
        f = open(file, "r")
        line_no = 0
        header = {"file_path": file}
        
        while True:

            line_no += 1

            line = (f.readline())
            line = line.strip()

            if line.startswith("radius"):
                line_info = line.split()
                header.update({"radius": np.double(line_info[1])})

            if line.startswith("earth_gravity_constant"):
                line_info = line.split()
                header.update({"earth_gravity_constant": np.double(line_info[1])})

            if line.startswith("max_degree"):
                line_info = line.split()
                header.update({"max_degree": int(line_info[1])})

            if line.startswith("time_coverage_start"):
                start_date, start_time = parse_datetime(line)
                header.update({"Start date": start_date,
                               "Start time": start_time})

            if line.startswith("time_coverage_end"):
                end_date, end_time = parse_datetime(line)
                header.update({"End date": end_date,
                               "End time": end_time})

            if line.startswith("key"):
                heading = ['key', 'L', 'M', 'C', 'S', 'sigma C', 'sigma S']
                header.update({"Heading": heading})

            if line.startswith("end_of_head"):
                header.update({"end_of_head": line_no})
                header_list.append(header)
                break

    return header_list
