#NEEDS WORK
#this file just reads in the initial coords, calls the simulation function
#then writes out the positions of the bodies!


#maybe constants should contain all the import files

#probably want the file read and write to be done using the method of the sim!

import csv #dont think this is used ever
import sims #terrible name -> change pls
import sys
#used for file input
import numpy as np
#used for deepcopying the solar_system!
import copy
import time


times = []
init_time = time.perf_counter()

#sets the start time to be zero

#argv[0] is name of file, dunno why that would ever be useful!
#reads in the command line arguments
#which includes the initial coord file, number of iterations and
#which sims to run
coord_file = sys.argv[1]
iters = int(sys.argv[2])
flags = sys.argv[3:]

#this is a constant
time_file = "source/results/time.txt"
output_file = "source/results/data.txt"
#this will change 
#unused I think
times_recorded = 7

#needs basic read write to be implemented
#otherwise works!
if "b" in flags:
    #resets the init time
    init_time = time.perf_counter()
    times = [0]
    #not implemented yet!
    #reads the file in and records the time
    ss = sims.base_read_file(coord_file)
    times.append(time.perf_counter()-init_time)

    #runs the sim
    ss, pos_history, b_sim_times = sims.basic_sim(ss, iters, init_time)
    #want some kind of path variable
    #keep these the same for now, having multiple doesn't help!
    b_time = times + b_sim_times

    #not implemted yet
    sims.base_write_to_file(output_file, pos_history)
    #records time taken to write data
    b_time.append(time.perf_counter()-init_time)
    #label pb = python basic
    sims.write_times('pb', b_time, time_file)


#works as intended I think
if "n" in flags:

    init_time = time.perf_counter()
    times = [0]
    ss = sims.numpy_read_file(coord_file)
    times.append(time.perf_counter()-init_time)

    #resets the init time
    ss, pos_history, n_sim_times = sims.numpy_sim(ss, iters, init_time)
    n_time = times + n_sim_times
    #want some kind of path variable
    output_file = "source/results/data.txt"
    sims.numpy_write_to_file(output_file, pos_history)
    #records time taken to write data
    n_time.append(time.perf_counter()-init_time)

    #label pn = python numpy
    sims.write_times('pn', n_time, time_file)


#mostly working
#needs its own read write implementation
#need to check this works for time implementation
if "m" in flags:
    #resets the init time
    init_time = time.perf_counter()
    times = [0]
    #reads the file and records the time taken
    ss = sims.multi_read_file(coord_file)
    times.append(time.perf_counter()-init_time)

    ss, pos_history, m_sim_times = sims.multi_sim(ss, iters, init_time)
    #want some kind of path variable
    #keep these the same for now, having multiple doesn't help!
    m_time = times + m_sim_times
    output_file = "source/results/data.txt"
    #shouldn't need this!
    pos_history = np.array(pos_history)
    sims.multi_write_to_file(output_file, pos_history)
    #records time taken to write data
    m_time.append(time.perf_counter()-init_time)
    #label pb = python basic
    sims.write_times('pm', m_time, time_file)


