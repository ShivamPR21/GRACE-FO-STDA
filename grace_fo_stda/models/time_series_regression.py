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
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from grace_fo_stda.physics.field import GravityField


class Model:
    """
    Class to define model, fit the input data, and reconstruct the time series
    """

    def __init__(self, grace_processor=GravityField()):
        self.grace_processor = grace_processor
        self.rfr_estimator = None
        self.linear_estimator = None
        self.poly_linear_estimator = None
        self.train_x = None
        self.train_y = None

    def load_data(self, smd):
        """
        Loads the SMD data from given smd dict
        :param smd: dict containing smd_info = {"header_info": anomalies["header_info"],
                                                "smd_anomaly": []}
        """
        # Define the training input x and y
        self.train_x = np.ones([len(self.grace_processor.smd_idx) * len(smd["header_info"]), 3])
        self.train_y = np.ones([len(self.grace_processor.smd_idx) * len(smd["header_info"]), ])
        sdl = len(self.grace_processor.smd_idx)

        # Arrange the data in the input format
        for i, (header, anomaly) in enumerate(zip(smd["header_info"], smd["smd_anomaly"])):
            self.train_x[sdl * i:sdl * (i + 1), 0] = (header["Start date"].year + header["Start date"].month / 12)
            self.train_x[sdl * i:sdl * (i + 1), 1] = self.grace_processor.lat
            self.train_x[sdl * i:sdl * (i + 1), 2] = self.grace_processor.long
            self.train_y[sdl * i:sdl * (i + 1), ] = np.float32(
                anomaly[self.grace_processor.smd_idx[:, 0], self.grace_processor.smd_idx[:, 1]]).flatten()
        self.train_y = self.train_y.ravel()

    def fit(self):
        """
        Fit the data to the model
        """

        # Generate polynomial features
        self.linear_estimator = LinearRegression().fit(self.train_x, self.train_y)
        poly_train_x = PolynomialFeatures().fit_transform(self.train_x)
        self.poly_linear_estimator = LinearRegression().fit(poly_train_x, self.train_y)
        self.rfr_estimator = RandomForestRegressor().fit(self.train_x, self.train_y)

    def reconstruct(self, x=None):
        """
        Reconstruct the results.
        :param x: Input data of size (sample, 3) containing time, lat, long
        :return: reconstructed data, y(smd)
        """
        if x is None:
            x = self.train_x

        poly_x = PolynomialFeatures().fit_transform(x)
        return ([self.rfr_estimator.predict(x), self.linear_estimator.predict(x),
                 self.poly_linear_estimator.predict(poly_x)])
