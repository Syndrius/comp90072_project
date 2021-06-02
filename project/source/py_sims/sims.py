#Written by Matthew Thomas 831343, May 2021 for COMP90072 at unimelb


import math
import numpy as np
import multiprocessing
import helper
import time


dt = 0.01
G = 2.96*10**(-4) #units of Au^3/solar mass/days^2

def basic_sim(ss, iters, init_time):
    print("Running basic simulation...")

    pos_history = []
    time_checks = []
    times = []

    #determines the points for recording the time
    for i in range(1, 5):
        time_checks.append(int(iters/5*i))

    for i in range(iters):
        
        if i in time_checks:
           times.append(time.perf_counter()-init_time) 
        
        ax, ay = basic_compute_a(ss)

        temp_list = []

        for j in range(len(ss[0])):
            
            ss[0][j] += ss[2][j]*dt
            ss[1][j] += ss[3][j]*dt

            ss[2][j] += ax[j]*dt
            ss[3][j] += ay[j]*dt
            temp_list.append(ss[0][j])
            temp_list.append(ss[1][j])

        pos_history.append(temp_list)

    #time that sim is complete
    times.append(time.perf_counter()-init_time) 
    return ss, pos_history, times


#computes the acceleration for the basic sim
def basic_compute_a(ss):

    num_coords = len(ss[0])
    ax = [0] * num_coords
    ay = [0] * num_coords

    #these get the acceleration of each body from all the other ones
    for j in range(num_coords):
        
        for k in range(j+1, num_coords):

            y_diff = ss[1][k] - ss[1][j] 
            x_diff = ss[0][k] - ss[0][j]

            angle = math.atan2(y_diff, x_diff)
            force = G*ss[4][j]*ss[4][k]/(x_diff**2 + y_diff**2)
            
            a1 = force/ss[4][j]
            a2 = force/ss[4][k]
            #updates the acceleration
            ax[j] += a1*math.cos(angle)
            ay[j] += a1*math.sin(angle)
            
            #updates the acceleration for the second body
            ax[k] += a2*math.cos(angle + math.pi)
            ay[k] += a2*math.sin(angle + math.pi)

    return ax, ay 


#Simulation using numpy
def numpy_sim(ss, iters, init_time):
    print("Running numpy simulation...")
    
    time_checks = []
    times = []

    #finds the points for recording times
    for i in range(1, 5):
        time_checks.append(int(iters/5*i))


    pos_history = np.zeros((iters, 2*len(ss[0])))

    for i in range(iters):

        if i in time_checks:
           times.append(time.perf_counter()-init_time) 

        ax, ay = numpy_compute_a(ss)
        #updates the ss
        ss[0] += ss[2]*dt
        ss[1] += ss[3]*dt
        ss[2] += ax*dt
        ss[3] += ay*dt
        
        #store as x y pairs for each body
        pos_history[i] = np.ravel([ss[0], ss[1]], 'F')

    #time that sim is complete
    times.append(time.perf_counter()-init_time) 

    return ss, pos_history, times


#computes the acceleration for the numpy sim
def numpy_compute_a(ss):

    #extra 'row' to create matrices for next calculation!
    x = ss[0:1]
    y = ss[1:2]
    mass = ss[4]
    
    #this creates pairwise distances between each body!
    dx = x.T - x
    dy = y.T - y
    
    #needs a softening, because it is calculating the acceleration due to itself
    inv_dist_cubed = (dx**2 + dy**2 + 0.000005**2)**(-1.5)
    
    #computes the acceleration
    ax = -G * (dx * inv_dist_cubed) @ mass
    ay = -G * (dy * inv_dist_cubed) @ mass

    return ax, ay


#Simulation using multiprocessing
def multi_sim(ss, iters, init_time):
    print("Running multiprocessing simulation...")

    time_checks = []
    times = []

    #finds the points for recording times
    for i in range(1, 5):
        time_checks.append(int(iters/5*i))

    #store the previous positions for plotting!
    pos_history = np.zeros((iters, 2*len(ss[0])))

    #creates the pool object of different processes
    with multiprocessing.Pool() as pool:

        for i in range(iters):

            if i in time_checks:
               times.append(time.perf_counter()-init_time) 
            #starmap, makes the 'pool' complete the function but with an iterable of 
            #args
            a = np.array(pool.starmap(multi_compute_a, [(ss, k) for k in range(len(ss[0]))]))
            
            ax = a[:,0]
            ay = a[:,1]
            
            #updates the ss object
            ss[0] += ss[2]*dt
            ss[1] += ss[3]*dt
            ss[2] += ax*dt
            ss[3] += ay*dt   
            
            #stores the history
            pos_history[i] = np.ravel([ss[0], ss[1]], 'F')

    #time that sim is complete
    times.append(time.perf_counter()-init_time) 

    return ss, pos_history, times


#computes the acceleration for the multi sim
def multi_compute_a(ss, body_index):

    #calculate a for this body
    main_body = ss[:,body_index]

    bodies = np.delete(ss, body_index, 1)
    
    x_diff = bodies[0] - main_body[0]
    y_diff = bodies[1] - main_body[1]
    
    #distance cubed!
    diff = (x_diff**2 + y_diff**2)**(-1.5)
    #temporary vector to make computing clearer
    temp = G*diff*bodies[4]
    ax = np.dot(x_diff,temp)
    ay = np.dot(y_diff, temp)
   
    return np.array([ax, ay])


