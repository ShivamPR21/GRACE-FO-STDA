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
from sklearn.ensemble import GradientBoostingRegressor

from grace_fo_stda.physics.field import GravityField


class model:
    """

    """
    def __init__(self, grace_processor=GravityField()):
        self.grace_processor = grace_processor
        self.estimator = None
        self.train_x = None
        self.train_y = None

    def fit(self, smd):
        """

        :param smd:
        """
        self.train_x = np.ones([len(self.grace_processor.smd_idx) * len(smd["header_info"]), 3])
        self.train_y = np.ones([len(self.grace_processor.smd_idx) * len(smd["header_info"]), 1])
        sdl = len(self.grace_processor.smd_idx)
        for i, (header, anomaly) in enumerate(zip(smd["header_info"], smd["smd_anomaly"])):
            self.train_x[sdl * i:sdl * (i + 1), 0] = (header["Start date"].year + header["Start date"].month / 12)
            self.train_x[sdl * i:sdl * (i + 1), 1] = self.grace_processor.lat
            self.train_x[sdl * i:sdl * (i + 1), 2] = self.grace_processor.long
            self.train_y[sdl * i:sdl * (i + 1), 0] = np.float32(
                anomaly[self.grace_processor.smd_idx[:, 0], self.grace_processor.smd_idx[:, 1]]).flatten()

        self.estimator = GradientBoostingRegressor(max_depth=1, random_state=0).fit(self.train_x, self.train_y)

    def reconstruct(self, x=None):
        """

        :param x:
        :return:
        """
        if x is not None:
            return self.estimator(x)
        else:
            return self.estimator(self.train_x)
