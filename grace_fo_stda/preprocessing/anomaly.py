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
Computes the anomaly for the given sc coefficients
"""

import numpy as np


def anomaly(sc_coeffs):
    """
    Computes the anomaly for the given sc coefficients
    :param sc_coeffs: sc coefficients
    :return: anomaly- {"header_info": [.....],
                         "sc_anomaly": [.....]}
    """

    # sc anomaly dict initialization
    sc_anomaly_coeffs = {"header_info": sc_coeffs["header_info"],
                         "sc_anomaly": np.array(sc_coeffs["sc_coeffs_mat"], np.float64)}

    for i in range(12):

        # Compute mean for the month i
        mean = np.zeros(np.shape(sc_coeffs["sc_coeffs_mat"][0]))
        n = 0
        idx = []
        for j, (header, sc) in enumerate(zip(sc_coeffs["header_info"], sc_coeffs["sc_coeffs_mat"])):
            if i + 1 == header["Start date"].month:
                # mean = (mean * n + sc) / (n + 1)
                mean[:, :, :2] = np.add(mean[:, :, :2], sc[:, :, :2])
                mean[:, :, 2:] = np.add(mean[:, :, 2:], np.square(sc[:, :, 2:]))
                n += 1
                idx.append(j)

        # mean of data and variance
        mean[:, :, :2] = np.divide(mean[:, :, :2], n)
        mean[:, :, 2:] = np.sqrt(np.divide(mean[:, :, 2:], n))

        tmp_mean = np.copy(mean)
        tmp_mean[np.where(np.abs(tmp_mean) < 1E-20)] = np.float(1E-26)

        idx = np.int32(idx)
        anomaly_tmp = np.zeros(np.shape(sc_coeffs["sc_coeffs_mat"][idx.astype(np.int32), :, :, :]),
                               dtype=np.float32)
        anomaly_tmp[:, :, :, :2] = np.subtract(np.array(sc_coeffs["sc_coeffs_mat"])[idx.astype(np.int32), :, :, :2],
                                               mean[:, :, :2])

        std = np.sqrt(np.add(np.square(np.array(sc_coeffs["sc_coeffs_mat"])[idx.astype(np.int32), :, :, 2:]),
                             np.square(mean[:, :, 2:])))

        anomaly_tmp[:, :, :, 2:] = std

        sc_anomaly_coeffs["sc_anomaly"][idx] = np.float64(anomaly_tmp)

    return sc_anomaly_coeffs
