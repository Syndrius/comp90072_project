
#this file works as intended atm
#bash script treats this properly, shouldn't need to be called again lol!
#this file is outdated big time!
#maybe fix this when the fastest sim is done, so that this can be done quickly!


import math
from constants import *
#import csv #dont think this is required
import core 

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



#runs the simulation once, to find the 'final positions' of the bodies
solar_system = core.run_simulation(solar_system, iters)


   
#reverses the direction of the bodies in the solar system
#so the simulation can be run backwards!
for i in solar_system:
    i.vx = -i.vx
    i.vy = -i.vy
    i.x_positions = [i.x]
    i.y_positions = [i.y]


#arbitrary choice for the asteroid's properties
#may want to include these inside constants.py later
asteroid_rad = 0.00005 #no idea what this is, may need to check it makes sense!
asteroid_mass = 10**(-20) #small mass so it has neglible effects on the rest of the solar system!
#will eventually want a radius for the asteroid and make it a bit more realistic!
#initial velocity components chosen through trial and error!
asteroid = core.celestial_body(solar_system[3].x+20*solar_system[3].radius, solar_system[3].y+20*solar_system[3].radius, 0.025, -0.008, asteroid_rad, asteroid_mass)

solar_system.append(asteroid)

#this is not super efficient as it treats the effect of the asteroid on the other planets 
#as non-zero
solar_system = core.run_simulation(solar_system, iters)



with open(coord_file, 'a') as f:
    f.write('{} {} {} {} {} {} \n'.format(solar_system[-1].x, solar_system[-1].y, -solar_system[-1].vx, -solar_system[-1].vy, solar_system[-1].radius, solar_system[-1].mass))


