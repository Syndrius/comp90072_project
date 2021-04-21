#this file just reads in the initial coords, calls the simulation function
#then writes out the positions of the bodies!


from constants import *
import csv
import core #terrible name -> change pls


###dt = 0.01
#at dt = 1 -> earth spirals inward -> demonstrates a minimum step_size for accuracy!

#coord_file = 'source/planet_coordinates.txt'
coord_file = 'source/' + planet_coord_file
#format of file may need more consideration, not sure if txt file is the best bet!

solar_system = []
with open(coord_file, 'r') as f:
        
    for line in f:

        #convert to float, may be a better way of doing this!
        coord_list = [float(i) for i in line.split()]
        #may not be the correct type, but not sure that will matter!
        solar_system.append(core.celestial_body(*coord_list))




solar_system = core.run_simulation(solar_system, iters)


#probably make this more specific to each program, eg body1_basic_py etc
#files to output results to!
coord_file_base = 'source/results/data_body_'


#not sure if this is the most efficient way of doing this, but should be alright!
#maybe should time this to make sure it isn't a big time sink!
for i in range(len(solar_system)):
    output_file_str = coord_file_base + str(i) + '.txt'
    #print(output_file)
    
    with open(output_file_str, 'w') as f:
        
        #good because it writes all the coordinates at once
        csv.writer(f, delimiter=' ').writerows(zip(solar_system[i].x_positions, solar_system[i].y_positions))
