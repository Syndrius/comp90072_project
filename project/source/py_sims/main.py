#NEEDS WORK
#this file just reads in the initial coords, calls the simulation function
#then writes out the positions of the bodies!



import sims 
import helper
import time
import sys
import numpy as np


times = []
init_time = time.perf_counter()


#reads in the command line arguments
#which includes the initial coord file, number of iterations and
#which sims to run
coord_file = sys.argv[1]
iters = int(sys.argv[2])
flags = sys.argv[3:]

#this is a constant
time_file = "source/results/time.txt"
output_file = "source/results/data.txt"

#needs basic read write to be implemented
#otherwise works!
if "b" in flags:
    #sets the init time
    init_time = time.perf_counter()
    times = [0]

    #reads the initial coordinates
    ss = helper.read_coord_file(coord_file)

    #runs the sim
    ss, pos_history, b_sim_times = sims.basic_sim(ss, iters, init_time)

    #combines the times
    b_time = times + b_sim_times

    #writes the position history to file
    helper.write_positions_to_file(output_file, np.array(pos_history))
    #records time taken to write data
    b_time.append(time.perf_counter()-init_time)
    
    #writes the times to file
    helper.write_times('pb', b_time, time_file)


#Runs the simulation using numpy
if "n" in flags:
    #sets the initial time
    init_time = time.perf_counter()
    times = [0]

    #reads the initial coordinates
    ss = helper.read_coord_file(coord_file)

    #runs the sim
    ss, pos_history, n_sim_times = sims.numpy_sim(ss, iters, init_time)
    n_time = times + n_sim_times

    #writes the position history to file
    helper.write_positions_to_file(output_file, pos_history)
    #records time taken to write data
    n_time.append(time.perf_counter()-init_time)

    #writes the time to file
    helper.write_times('pn', n_time, time_file)


#Runs the simulation using multiprocessing
if "m" in flags:
    #sets the init time
    init_time = time.perf_counter()
    times = [0]
    #reads the initial coordinates
    ss = helper.read_coord_file(coord_file)

    #runs the sim
    ss, pos_history, m_sim_times = sims.multi_sim(ss, iters, init_time)
    m_time = times + m_sim_times

    #writes the position history to file
    helper.write_positions_to_file(output_file, pos_history)
    #records time taken to write data
    m_time.append(time.perf_counter()-init_time)

    #writes the time to file
    helper.write_times('pm', m_time, time_file)

