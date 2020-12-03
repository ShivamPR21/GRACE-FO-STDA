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


class EarthPrams:
    """
    Class containing earth representation related parameters.\n
    Presently based on WGS84.\n
    """

    def __init__(self):
        # WGS84 ellipsoid representation of earth
        self.rho = np.float32(5515)
        self.a = np.float32(6378137)
        self.GM = np.float32(3986004.418E8)
        self.f_inv = np.float32(298.257223563)
        self.b = self.a * (self.f_inv - 1) / self.f_inv
        self.R = (2 * self.a + self.b) / 3
