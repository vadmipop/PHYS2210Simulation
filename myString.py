import copy
import time

import numpy as np
import json
from Constants import *


def copy_array(array):
    new_array = np.empty_like(array)
    np.copyto(new_array, array)
    return new_array


class InitFail(Exception):
    pass


class String(object):
    def __init__(self, t, n_pts, conf_type, rho, rho_bead):
        self.tension = t
        self.n_pts = n_pts
        self.rho = rho
        self.rho_bead = rho_bead
        self.prev_disp_list = np.zeros(n_pts)
        self.curr_disp_list = np.zeros(
            n_pts
        )  # important to keep in mind that it's an ndarray
        self._bead_pos_list_init(
            conf_type
        )  # beads_pos_list is a regular python array, not ndarray
        self._dens_list_init(n_pts)  # dens_list is an ndarray
        # ------------- the following stuff is for graphing purposes -----------------

    def update(self, start_time):
        prev_list = copy_array(self.prev_disp_list)
        cur_list = copy_array(self.curr_disp_list)
        self.prev_disp_list = copy_array(self.curr_disp_list)
        self.curr_disp_list[0] = Y_D * np.sin(OMEGA * (time.time() - start_time))
        for i in range(1, self.curr_disp_list.size - 1):
            self.curr_disp_list[i] = (
                2 * cur_list[i]
                - prev_list[i]
                + (
                    TENSION
                    * (DELTA_T ** 2)
                    * (cur_list[i - 1] + cur_list[i + 1] - 2 * cur_list[i])
                )
                / (self.dens_list[i] * ((L / N_PTS) ** 2))
            )

    def get_disp(self, i):
        return self.curr_disp_list[i]

    def get_disp_list(self):
        return self.curr_disp_list

    def get_period(self):
        return self.period

    def _bead_pos_list_init(self, conf_type):
        self.bead_pos_list = []
        self._bead_pos_list_from_json(conf_type)  # let's assume this works properly...

    def _bead_pos_list_from_json(self, conf_type):
        """
        Initializes the list of positions of beads from json. Raises InitFail() if the appropriate
        bead configuration is not found in the json file.
        """
        success = 0
        with open("data/beads.json") as beads_json:
            beads = json.load(beads_json)
            configs = beads["configurations"]
            for index in range(len(configs)):
                if configs[index]["type"] == conf_type:
                    self.bead_pos_list = configs[index]["beads_pos"]
                    self.period = configs[index]["fundamental_period"]
                    success = 1
        if success == 1:
            pass
        else:
            raise InitFail()

    def _dens_list_init(self, n_pts):
        """
        Initializes the list that contains mass densities at various points along the string.
        Assumes that the elements of self.bead_pos_list are integer in range(0, n_pts).
        :param n_pts: The number of points along the string we keep track of.
        :return: None
        """
        self.dens_list = np.zeros(n_pts)
        self.dens_list[0] = self.rho
        for i in range(n_pts - 1):
            if i in self.bead_pos_list:
                self.dens_list[i] = self.rho_bead
            else:
                self.dens_list[i] = self.rho
        self.dens_list[n_pts - 1] = self.rho
