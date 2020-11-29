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

import numpy as np


def anomaly(sc_coeffs):
    """

    :param sc_coeffs:
    :return:
    """

    sc_anomaly_coeffs = {"header_info": sc_coeffs["header_info"],
                         "sc_anomaly_abs_log": np.array(sc_coeffs["sc_coeffs_mat"], np.float64),
                         "sc_anomaly_sign": np.zeros(np.shape(sc_coeffs["sc_coeffs_mat"]))}

    for i in range(12):
        mean = 0
        n = 0
        idx = []
        for j, (header, sc) in enumerate(zip(sc_coeffs["header_info"], sc_coeffs["sc_coeffs_mat"])):
            if i + 1 == header["Start date"].month:
                mean = (mean * n + sc) / (n + 1)
                n += 1
                idx.append(j)

        idx = np.int32(idx)
        #
        # for j, (header, sc) in enumerate(zip(sc_coeffs["header_info"], sc_coeffs["sc_coeffs_mat"])):
        #     if i + 1 == header["Start date"].month:
        anomaly_tmp = np.array(sc_coeffs["sc_coeffs_mat"])[idx.astype(np.int32)] - mean
        anomaly_tmp[np.where(np.abs(anomaly_tmp) <= np.float64(1E-20))] = np.float64(1E-26)
        sc_anomaly_coeffs["sc_anomaly_abs_log"][idx] = np.log10(np.abs(anomaly_tmp))
        sc_anomaly_coeffs["sc_anomaly_sign"][idx] = np.sign(anomaly_tmp)

    return sc_anomaly_coeffs
