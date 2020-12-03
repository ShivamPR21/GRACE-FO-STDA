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
Read actual data about Spherical Harmonics with the help of header information.
"""

import numpy as np
import pandas as pd

from grace_fo_stda.grace_read.read_header import read_header


def read(files):
    """
    :param files: List of files to be read
    :return: Dict containing header information as list and coefficients as list matrices
                {"header_info": ,
                "sc_coeffs_mat": }
    """
    # Temporal anomalies as dictionary
    temporal_anomaly = {"header_info": [],
                        "sc_coeffs_mat": []}

    # Read header information about all the files
    header_info = read_header(files)
    temporal_anomaly.update({"header_info": header_info})

    for i, header in enumerate(header_info):
        sc_coeff_mat = np.zeros([header["max_degree"] + 1, header["max_degree"] + 1, 4])
        # Get the file name
        file_path = header["file_path"]
        skip_lines = header["end_of_head"]

        # Read Spherical Harmonic Coefficients from file
        lmsc_coeffs = pd.read_csv(file_path, sep='\s+', skiprows=skip_lines, header=None)

        idx = np.int32(lmsc_coeffs.iloc[:, 1:3].values)
        # print(idx)
        sc_coeff_mat[idx[:, 0], idx[:, 1]] = np.float64(lmsc_coeffs.iloc[:, 3:].values)

        temporal_anomaly["sc_coeffs_mat"].append(sc_coeff_mat)

    temporal_anomaly["sc_coeffs_mat"] = np.float64(temporal_anomaly["sc_coeffs_mat"])

    return temporal_anomaly
