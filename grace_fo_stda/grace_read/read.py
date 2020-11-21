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
Read actual data about Spherical Harmonics with the help of header information.
"""

import pandas as pd
import numpy as np
from grace_fo_stda.grace_read.read_header import read_header


def read(files):
    # Temporal anomalies as dictionary
    temporal_anomaly = {"header_info": [],
                        "sc_coeffs_mat": []}

    # Read header information about all the files
    header_info = read_header(files)
    temporal_anomaly.update({"header_info": header_info})

    sc_coeff_mat = np.zeros([header_info["max_degree"], header_info["max_degree"], 4])

    for i, header in enumerate(header_info):
        # Get the file name
        file_path = header["file_path"]
        skip_lines = header["end_of_head"]

        # Read Spherical Harmonic Coefficients from file
        lmsc_coeffs = pd.read_csv(file_path, sep='\s+', skiprows=skip_lines, header=None)

        idx = np.int32(lmsc_coeffs.iloc[:, 1:3].values)
        sc_coeff_mat[idx] = np.float64(lmsc_coeffs.iloc[:, 3:].values)

        temporal_anomaly.update({"sc_coeffs_mat": (temporal_anomaly["sc_coeffs_mat"].append(sc_coeff_mat))})

    return temporal_anomaly
