#Written by Matthew Thomas 831343, May 2021 for COMP90072 at unimelb

#This file contains helper function for the python simulations

import time
import numpy as np


#reads the coordinate file
# returns an array of form ss[0] = x, ss[1] = y, ss[2] = vx, ss[3] = vy, ss[4] = mass

def read_coord_file(file_name):
    return np.loadtxt(file_name).T

#writes the position history to file
def write_positions_to_file(file_name, pos):
    np.savetxt(file_name, pos)


#writes the times to file
def write_times(label, times, time_file):
    with open(time_file, "a") as f:
        print(*times, label, file=f)

