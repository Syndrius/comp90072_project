import numpy as np
from constants import *


#should not be here, need to start passing values around properly!
dt = 0.01

def run_simulation(solar_system, iters):
    #first take the solar system object then create numpy arrays to use for the sim
    
    #(x,y) for each body
    pos = np.zeros((len(solar_system), 2))
    vel = np.zeros((len(solar_system), 2))
    mass = np.zeros(len(solar_system))

    #may need to convert vel to centre of mass if following code!

    #these should be small loops just to initialise!

    for i in range(len(solar_system)):
        
        pos[i][0] = solar_system[i].x
        pos[i][1] = solar_system[i].y
        
        vel[i][0] = solar_system[i].vx
        
        vel[i][1] = solar_system[i].vy
        mass[i] = solar_system[i].mass


    #store the previous positions for plotting!
    past_x = np.zeros((iters, len(solar_system)))
    past_y = np.zeros((iters, len(solar_system)))


    for i in range(iters):
        acc = compute_a(pos, mass)
        pos += vel*dt
        vel += acc*dt

        past_x[i] = pos[:,0]
        past_y[i] = pos[:,1]

    

    #updates the original object and returns that!

    for i in range(len(solar_system)):
        solar_system[i].x = pos[i][0]
        solar_system[i].y = pos[i][1]
        solar_system[i].vx = vel[i][0]
        solar_system[i].vy = vel[i][1]
        solar_system[i].x_positions = past_x[:,i]
        solar_system[i].y_positions = past_y[:,i]


    return solar_system

    #note this works slightly different to other sim, doesn;t use an angle!
    #instead does (r_i - r_j)/|r_i-r_j|^3
    #may want to swap all of them to this for consistancy!
    #numpy has an atan2 then can be vectorised! -> use that instead!


def compute_a(pos, mass):

    #extra 'row' to create matrices for next calculation!
    x = pos[:, 0:1]
    y = pos[:, 1:2]
    
    #this creates pairwise distances between each body!
    dx = x.T - x
    dy = y.T - y
    
    
    #need magnitude?
    #needs a softening, I think because it is calculating the acceleration due to itself!
    #without value it just gives nan everywhere!
    inv_dist_cubed = (dx**2 + dy**2 + 0.000005**2)**(-1.5)
    
    ax = G * (dx * inv_dist_cubed) @ mass
    ay = G * (dy * inv_dist_cubed) @ mass
    
    #this combines them, not certain about the final form though!
    a = np.column_stack((ax, ay))

    return a

