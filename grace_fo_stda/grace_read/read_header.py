#!/usr/bin/env python3
#
# Copyright 2020 Shivam Pandey
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Header information retrieval for further data processing and directly reading useful information of Spherical Harmonic
Coefficients.
"""

import re
from datetime import datetime


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
        header = {"file_name": file}
        while True:

            line_no += 1

            line = (f.readline())
            line = line.strip()

            if line.startswith("time_coverage_start"):
                line_info = re.split(": |T", line)
                start_date = datetime.strptime(line_info[1].strip(), "%Y-%m-%d").date()
                start_time = datetime.strptime(line_info[2].strip(), "%H:%M:%S.%f").time()
                header.update({"Start date": start_date,
                               "Start time": start_time})

            if line.startswith("time_coverage_end"):
                line_info = re.split(": |T", line)
                end_date = datetime.strptime(line_info[1].strip(), "%Y-%m-%d").date()
                end_time = datetime.strptime(line_info[2].strip(), "%H:%M:%S.%f").time()
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
