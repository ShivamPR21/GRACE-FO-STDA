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

import os

import numpy as np
import pandas as pd
import scipy.io as sio
from pyshtools.expand import spharm

from .earthprams import EarthPrams


class GravityField(EarthPrams):
    """
    Class to compute the gravity field related quantities\n
    Only SMD(Surface mass density) is implented for mote request on gitlab.com/ShivamPR21
    """

    def __init__(self):
        self.idx, self.lat, self.long = None, [], []
        self.raster_map = []
        self.catchment_info = []
        self.dir_path = os.path.realpath(__file__).replace("field.py", "")
        super(GravityField, self).__init__()
        self.love_number = self.load_love_number()
        self.smd_idx = []

    def load_love_number(self):
        """
        Loads love number from love_numbers.xlsx
        :return:
        """
        love_number = np.float32(pd.read_csv(self.dir_path + "/params/love_numbers.csv").values)
        return np.float32(love_number)

    def load_location_mask(self, loc, res=0.5):
        """
        Loads location mask for the  specified catchment area to be studied
        :param loc: String, Location name
        :param res: Float, Resolution of map 1 grid = res deg
        """
        self.raster_map = sio.loadmat(self.dir_path + "/params/ctchmntindx3.mat")
        self.catchment_info = sio.loadmat(self.dir_path + "/params/ctchnms.mat")["ctchnms"]
        catchment = np.concatenate(self.catchment_info[:, 0]).ravel()
        idx = np.concatenate(self.catchment_info[:, 3]).ravel()[np.where(catchment == loc)]

        self.lat, self.long = np.where(self.raster_map["cindx3"] == idx)

        self.smd_idx = np.int32([self.lat - np.min(self.lat), self.long - np.min(self.long)]).T

        # Bring the latitude in range [0, pi]
        self.lat = np.float32(self.lat)
        self.lat *= res * np.pi / 180

        # Being the longitude in range [0, 2pi]
        self.long = np.float32(self.long)
        self.long *= res * np.pi / 180
        self.long -= np.pi
        self.long[np.where(self.long < 0)] += 2 * np.pi

    def smd(self, anomalies):
        """
        Computes SMD for the given filtered or unfiltered sc_anomalies
        :param anomalies: dict{"header_info": [....],
                                "sc_anomaly": [....]}
        :return: smd = {"header_info": [....],
                        "smd_anomaly": [....]}
        """

        # Variable definition
        max_l, l, m = None, None, None
        pre_multiplier = None
        ylmc, ylms = [], []

        smd_info = {"header_info": anomalies["header_info"],
                    "smd_anomaly": []}

        for i, (header, anomaly) in enumerate(
                zip(anomalies["header_info"], anomalies["sc_anomaly"])):

            # Compute the Ylm coeffs for defined lat, long
            if max_l != header["max_degree"]:
                max_l = header["max_degree"]
                l_range = np.arange(0, max_l + 1)

                # Pre-multiplier transform computation (2*l+1)/(1+k_l)
                pre_multiplier = np.float64(
                    [(2 * l_range + 1) / (
                            1 + np.interp(l_range, self.love_number[:, 0], self.love_number[:, 1]))]).T.reshape(
                    max_l + 1, 1)

                #  Compute Ylm
                for (lat, long) in zip(self.lat, self.long):
                    ylm = spharm(max_l, long, lat, '4pi', 'real', 1, False, False)
                    ylmc_ = ylm[0, :, :]
                    ylms_ = ylm[1, :, :]
                    ylmc.append(ylmc_)
                    ylms.append(ylms_)

            # Initialize smd grid and compute the smd values for land mass
            smd_grid = np.zeros([np.max(self.smd_idx[:, 0]) + 1, np.max(self.smd_idx[:, 1]) + 1], dtype=np.float64)
            act_anomaly = anomaly

            for (smd_idx, ylmc_, ylms_) in zip(self.smd_idx, ylmc, ylms):
                tmp_act_anomaly = np.zeros(np.shape(act_anomaly))
                tmp_act_anomaly[:, :, 0], tmp_act_anomaly[:, :, 1] = \
                    np.multiply(ylmc_, act_anomaly[:, :, 0]), np.multiply(ylms_, act_anomaly[:, :, 1])

                sum_tmp = np.sum(tmp_act_anomaly[:, :, :2], axis=2)

                sum_tmp = np.sum(sum_tmp, axis=1, keepdims=True)

                sum_tmp = np.sum(np.multiply(pre_multiplier, sum_tmp))

                smd_grid[smd_idx[0], smd_idx[1]] = -(self.R * self.rho / 3) * sum_tmp

            # Update smd information
            smd_info["smd_anomaly"].append(smd_grid)

        # return smd_info = {"header_info": [.....],
        #                     "smd_anomaly": [.....]}
        return smd_info
