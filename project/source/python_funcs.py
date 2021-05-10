#NEEDS WORK
#this will be the basic file that stores the classes and the functions that are used by everything!
import math
#need to determine where the imports should be!

import numpy as np
import multiprocessing

#shouldn't be doing this here!
import time

#form of solar system array!
#ss[0] = x, ss[1] = y, ss[2] = vx, ss[3] = vy, ss[4] = mass

dt = 0.01
G = 2.96*10**(-4) #units of Au^3/solar mass/days^2
#at dt = 1 -> earth spirals inward -> demonstrates a minimum step_size for accuracy!

def basic_sim(ss, iters, init_time):
    print("Running basic simulation...")

    pos_history = []
    time_checks = []
    times = []

    #no good atm 
    #needs to be changed
    #determines the points for recording the time
    for i in range(1, 5):
        time_checks.append(int(iters/5*i))

    for i in range(iters):
        
        if i in time_checks:
           times.append(time.perf_counter()-init_time) 
        
        ax, ay = basic_compute_a(ss)

        temp_list = []
        #maybe want another function called update
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

    #these get the acceleration of each body from all the other ones!
    for j in range(num_coords):
        
        for k in range(j+1, num_coords):

            y_diff = ss[1][k] - ss[1][j] 
            x_diff = ss[0][k] - ss[0][j]

            angle = math.atan2(y_diff, x_diff)
            force = G*ss[4][j]*ss[4][k]/(x_diff**2 + y_diff**2)
            
            a1 = force/ss[4][j]
            a2 = force/ss[4][k]
            #not entirely clear why we need the pi here lol
            ax[j] += a1*math.cos(angle)
            ay[j] += a1*math.sin(angle)
            
            #finds the acceleration of the other body
            ax[k] += a2*math.cos(angle + math.pi)
            ay[k] += a2*math.sin(angle + math.pi)

    return ax, ay 



def numpy_sim(ss, iters, init_time):
    print("Running numpy simulation...")
    
    time_checks = []
    times = []

    #no good atm 
    #needs to be changed
    #may be better for this to be passed in
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


def numpy_compute_a(ss):

    #extra 'row' to create matrices for next calculation!
    x = ss[0:1]
    y = ss[1:2]
    mass = ss[4]
    
    #this creates pairwise distances between each body!
    dx = x.T - x
    dy = y.T - y
    
    #needs a softening, I think because it is calculating the acceleration due to itself!
    #without value it just gives nan everywhere!
    inv_dist_cubed = (dx**2 + dy**2 + 0.000005**2)**(-1.5)
    
    #negs in here are required, could swap to x - x.T
    ax = -G * (dx * inv_dist_cubed) @ mass
    ay = -G * (dy * inv_dist_cubed) @ mass

    return ax, ay


#works!
def multi_sim(ss, iters, init_time):
    print("Running multiprocessing simulation...")

    time_checks = []
    times = []
    #no good atm 
    #needs to be changed
    #may be better for this to be passed in
    for i in range(1, 5):
        time_checks.append(int(iters/5*i))

   #store the previous positions for plotting!
    
    pos_history = np.zeros((iters, 2*len(ss[0])))

    with multiprocessing.Pool() as pool:

        for i in range(iters):

            if i in time_checks:
               times.append(time.perf_counter()-init_time) 
            #note there should be an if __name__==__main__ thing here
            #but doesnt work in not main file
            #starmap, makes the 'pool' complete the function but with an iterable of 
            #args
            results = np.array(pool.starmap(multi_compute_a, [(ss, k) for k in range(len(ss[0]))]))
            
            ax = results[:,0]
            ay = results[:,1]

            ss[0] += ss[2]*dt
            ss[1] += ss[3]*dt
            ss[2] += ax*dt
            ss[3] += ay*dt   

            pos_history[i] = np.ravel([ss[0], ss[1]], 'F')

    #time that sim is complete
    times.append(time.perf_counter()-init_time) 

    return ss, pos_history, times


def multi_compute_a(ss, body_index):

    #calculate a for this body
    main_body = ss[:,body_index]

    bodies = np.delete(ss, body_index, 1)
    
    x_diff = bodies[0] - main_body[0]
    #print(x_diff)
    y_diff = bodies[1] - main_body[1]
    
    #distance cubed!
    diff = (x_diff**2 + y_diff**2)**(-1.5)
    #temporary vector to make computing clearer
    temp = G*diff*bodies[4]
    ax = np.dot(x_diff,temp)
    ay = np.dot(y_diff, temp)
   
    return np.array([ax, ay])

#basic python way of reading file
#needs to be implmented
def base_read_file(file_name):
    x = []
    y = []
    vx = []
    vy = []
    mass = []
    with open(file_name) as f:
        for line in f:
            line_list = line.split()
            x.append(float(line_list[0]))
            y.append(float(line_list[1]))
            vx.append(float(line_list[2]))
            vy.append(float(line_list[3]))
            mass.append(float(line_list[4]))

    return [x, y, vx, vy, mass]

#uses numpy to read the initial_coord file
#note multiprocessing uses this!
def numpy_read_file(f):
    return np.loadtxt(f).T

#this will be really ineficient!
def multi_read_file(file_name):
    return numpy_read_file(file_name)

#needs to be implemented
def base_write_to_file(file_name, pos):
    pos = np.array(pos)
    return numpy_write_to_file(file_name, pos)
def numpy_write_to_file(file_name, pos):
    np.savetxt(file_name, pos)

#placeholder, needs to be implemented!
def multi_write_to_file(file_name, pos):
    return numpy_write_to_file(file_name, pos)

def write_times(label, times, time_file):
    with open(time_file, "a") as f:
        print(*times, label, file=f)

