import time

import numpy as np

import myString
import matplotlib.pyplot as plt
from Constants import *

flag1 = False
flag2 = False
flag3 = False
x1 = np.linspace(0, L, N_PTS)
x2 = np.linspace(0, L, N_PTS)
x3 = np.linspace(0, L, N_PTS)


def zero_of_x(x):
    return 0


if __name__ == "__main__":
    time_print = 0
    start_time = time.time()
    string = myString.String(TENSION, N_PTS, CONF_TYPE, RHO, RHO_BEAD)
    while time.time() - start_time < SIM_TIME:
        time_now = time.time()
        # the next if statement is for assessing how adequate the model is
        # if time.time() - start_time > time_print * 1:
        #     print(string.get_disp(0), string.get_disp(1))
        #     time_print += 1
        string.update(start_time)
        if (
            flag1 == False
            and time_now - (start_time + T_SAMPLE) < string.get_period() / 3
        ):
            y1 = string.get_disp_list()
            flag1 = True
        if (
            flag2 == False
            and string.get_period() / 3
            <= time_now - (start_time + T_SAMPLE)
            < 2 * string.get_period() / 3
        ):
            y2 = string.get_disp_list()
            flag2 = True
        # if (
        #     flag3 == False
        #     and 2 * string.get_period() / 3
        #     <= time_now - (start_time + T_SAMPLE)
        #     < string.get_period()
        # ):
        #     y3 = string.get_disp_list()
        #     flag3 = True
        time.sleep(DELTA_T - (time.time() - time_now))
    plt.plot(x1, y1, "red")
    plt.plot(x1, y2, "blue")
    plt.plot(x1, [zero_of_x(x) for x in x1], "g--")
    plt.show()
    # plt.savefig("Plot.jpeg", bbox_inches="tight")
