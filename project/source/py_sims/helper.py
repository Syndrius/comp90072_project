import time
import numpy as np


#reads the coordinate file
def read_coord_file(file_name):
    return np.loadtxt(file_name).T

#writes the position history to file
def write_positions_to_file(file_name, pos):
    np.savetxt(file_name, pos)


#writes the times to file
def write_times(label, times, time_file):
    with open(time_file, "a") as f:
        print(*times, label, file=f)

