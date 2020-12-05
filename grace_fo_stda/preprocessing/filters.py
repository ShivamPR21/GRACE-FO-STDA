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
Filter the data read by grace_read function
"""

from copy import copy

import numpy as np
from scipy.ndimage.filters import gaussian_filter1d


def gauss_filter(sc_anomaly, gaussian_blur=np.float32([None, None])):
    """

    :param sc_anomaly: anomaly dict
    :param gaussian_blur:
    :return:
    """
    sc_anomaly_tmp = copy(sc_anomaly)
    for i, (header, sc) in enumerate(zip(sc_anomaly_tmp["header_info"], sc_anomaly_tmp["sc_anomaly"])):
        m_max = np.shape(sc)[1]

        sc = np.float64(sc)
        sc_tmp = np.concatenate((np.fliplr(sc[:, 1:, 1]), sc[:, :, 0]), axis=1)

        mask = copy(sc_tmp)
        mask[np.where(sc_tmp < -18)] = 0
        mask[np.where(sc_tmp >= -18)] = 1

        if gaussian_blur[0] is not None:
            sc_tmp = gaussian_filter1d(sc_tmp * mask, sigma=gaussian_blur[0], axis=1)
        else:
            raise (ValueError("Provide the horizontal blur value."))

        if gaussian_blur[1] is not None:
            sc_tmp = gaussian_filter1d(sc_tmp * mask, sigma=gaussian_blur[1], axis=0) + np.invert(
                mask.astype(np.bool)).astype(np.int8) * (-26)

        sc_anomaly_tmp["sc_anomaly"][i][:, 1:, 1] = np.fliplr(sc_tmp[:, :m_max - 1])
        sc_anomaly_tmp["sc_anomaly"][i][:, :, 0] = sc_tmp[:, m_max - 1:]

    return sc_anomaly_tmp
