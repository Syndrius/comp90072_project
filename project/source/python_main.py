#this file just reads in the initial coords, calls the simulation function
#then writes out the positions of the bodies!


#maybe constants should contain all the import files
from constants import *

import csv
import python_sims #terrible name -> change pls
import sys
#used for file input
import numpy as np
#used for deepcopying the solar_system!
import copy




###dt = 0.01
#at dt = 1 -> earth spirals inward -> demonstrates a minimum step_size for accuracy!

#coord_file = 'source/planet_coordinates.txt'
coord_file = 'source/' + planet_coord_file
#format of file may need more consideration, not sure if txt file is the best bet!

#coord_file must always be read I think
#maybe this will change if we are just making an arbitrary n-body_problem
solar_system_init = []
with open(coord_file, 'r') as f:
        
    for line in f:

        #convert to float, may be a better way of doing this!
        coord_list = [float(i) for i in line.split()]
        #may not be the correct type, but not sure that will matter!
        solar_system_init.append(python_sims.celestial_body(*coord_list))

#may want the celestial body class defined here!!!!
#might be best to just have two files, this one as the 'main' that reads and writes files
#and controls which sims are done
#then the simulation file which just contains function for each sim
#that will also prevent the solar_system object from running each time!

#writes the position history to the given file
def write_to_file(file_name, positions):
    np.savetxt(file_name, positions)



#hopefully solar_system_init isnt written over!

if "b" in sys.argv:
    solar_system, pos_history = python_sims.basic_sim(solar_system_init, iters)
    #want some kind of path variable
    #keep these the same for now, having multiple doesn't help!
    output_file = "source/results/data.txt"
    pos_history = np.array(pos_history)
    write_to_file(output_file, pos_history)


if "n" in sys.argv:
    solar_system, pos_history = python_sims.numpy_sim(solar_system_init, iters)
    #want some kind of path variable
    output_file = "source/results/data.txt"
    write_to_file(output_file, pos_history)


#just have a write_to_file here, as they should all write to same place



#testing the numpy version
#takes sim from ~1:20 to ~30
#simulation looks good! woo
#solar_system = numpy_sim.run_simulation(solar_system_init, iters)

#probably make this more specific to each program, eg body1_basic_py etc
#files to output results to!
coord_file_base = 'source/results/data_body_'

#not sure if this is the most efficient way of doing this, but should be alright!
#maybe should time this to make sure it isn't a big time sink!
'''
for i in range(len(solar_system)):
    output_file_str = coord_file_base + str(i) + '.txt'
    #print(output_file)
    
    with open(output_file_str, 'w') as f:
        
        #good because it writes all the coordinates at once
        csv.writer(f, delimiter=' ').writerows(zip(solar_system[i].x_positions, solar_system[i].y_positions))
        '''
