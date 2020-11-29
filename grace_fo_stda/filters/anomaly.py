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

def anomaly(sc_coeffs):
    """

    :param sc_coeffs:
    :return:
    """

    sc_coeffs_tmp = sc_coeffs.copy()
    for i in range(12):
        mean = 0
        n = 0
        for header, sc in zip(sc_coeffs_tmp["header_info"], sc_coeffs_tmp["sc_coeffs_mat"]):
            if i+1 == header["Start date"].month:
                mean = (mean * n + sc) / (n + 1)
                n += 1

        for j, (header, sc) in enumerate(zip(sc_coeffs_tmp["header_info"], sc_coeffs_tmp["sc_coeffs_mat"])):
            if i+1 == header["Start date"].month:
                sc_coeffs_tmp["sc_coeffs_mat"][j] = sc-mean

    return sc_coeffs_tmp
