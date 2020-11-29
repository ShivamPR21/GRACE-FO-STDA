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

import numpy as np
from scipy.ndimage.filters import gaussian_filter
from matplotlib import pyplot as plt


def gauss_filter(sc_anomaly, gaussian_blur=None):
    """

    :param sc_anomaly: anomaly dict
    :param gaussian_blur:
    :return:
    """
    sc_anomaly_tmp = sc_anomaly.copy()
    for i, (header, sc) in enumerate(zip(sc_anomaly_tmp["header_info"], sc_anomaly_tmp["sc_coeffs_mat"])):
        m_max = np.shape(sc)[1]

        sc = np.float64(sc)
        sc_tmp = np.concatenate((np.fliplr(sc[:, 1:, 1]), sc[:, :, 0]), axis=1)

        mask = np.zeros(np.shape(sc_tmp))
        mask[np.nonzero(sc_tmp)] = 1

        sc_tmp_filtered = gaussian_filter(sc_tmp * mask, sigma=gaussian_blur)
        weights = gaussian_filter(mask, sigma=gaussian_blur)
        sc_tmp_filtered /= weights
        # after normalized convolution, you can choose to delete any data outside the mask:
        sc_tmp_filtered *= mask

        sc_anomaly_tmp["sc_coeffs_mat"][i][:, 1:, 1] = np.fliplr(sc_tmp_filtered[:, :m_max - 1])
        sc_anomaly_tmp["sc_coeffs_mat"][i][:, :, 0] = sc_tmp_filtered[:, m_max - 1:]

    return sc_anomaly_tmp
