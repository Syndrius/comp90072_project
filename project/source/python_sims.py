#this will be the basic file that stores the classes and the functions that are used by everything!
import math
from constants import * #think this is purely for G -> could be better to redefine
import numpy as np

#shouldn't be doing this here!
import time

###dt = 0.01
#at dt = 1 -> earth spirals inward -> demonstrates a minimum step_size for accuracy!

class celestial_body:


    def __init__(self, x, y, vx, vy, radius, mass):

        #are any of these comments needed?

        #initial x and y coordinates of the celestial body
        self.x = x
        self.y = y

        #initial x and y velocity coordinates of the celestial body
        self.vx = vx
        self.vy = vy

        #initial x and y acceleration coordinates of the celestial body
        #maybe dont need an accelration here, just work with force and divide by mass within class!
        self.ax = 0 #not sure if an initial acceleration is needed tbh!
        self.ay = 0

        #initialise the colour and size of the planet
        self.radius = radius
        self.mass = mass
        #self.colour = colour #used for plotting!

    #not sure this is how dt should be passed around, maybe should be h instead?
    def update_velocity(self, dt):
        self.vx += self.ax*dt
        self.vy += self.ay*dt
        #self.reset_acceleration()

    #really don't think dt should be passed in, surely it is a constant??
    def update_position(self, dt):
        self.x += self.vx*dt
        self.y += self.vy*dt

    #reset the acceleration between iterations
    def reset_acceleration(self):
        self.ax = 0
        self.ay = 0



#the basic simulation function, takes a list of celestial bodies
#and the number of iterations!
def basic_sim(solar_system, iters, init_time):
    print("Running basic simulation...")

    pos_history = []

    time_checks = []
    times = []
    #no good atm 
    #needs to be changed
    for i in range(1, 5):
        time_checks.append(int(iters/5*i))

    for i in range(iters):

        if i in time_checks:
           times.append(time.perf_counter()-init_time) 
        
        #may need to check these loops
        #these get the acceleration of each body from all the other ones!
        for j in range(len(solar_system)):
            body1 = solar_system[j]
            
            #print(bodies[j])
            
            for k in range(j+1, len(solar_system)):
                body2 = solar_system[k]
                #print(bodies[j], bodies[k])
        
                y_diff = body2.y - body1.y

                x_diff = body2.x - body1.x
                #print(y_diff, x_diff)
                #print('Sun pos: ', Sun.x, Sun.y)
                #print('Eath pos ', Earth.x, Earth.y)

                #need to apply some sort of test to check if planets have collided!
                #can test this by introducing a massive asteroid!


                #thingo has (y,x) but surely it should be x, y?
                #try to undertsand what is actually going on here 
                angle = math.atan2(y_diff, x_diff)
                #print('Angle:', angle)
                #should make sure this is correct 
                force = G*body1.mass*body2.mass/(x_diff**2 + y_diff**2)
                
                a1 = force/body1.mass
                a2 = force/body2.mass
                #print(Sun.mass)
                #print(G, Sun.mass, Earth.mass, x_diff, y_diff)
                #print('Force: ',force)
                
                #not entirely clear why we need the pi here lol
                body1.ax += a1*math.cos(angle)
                body1.ay += a1*math.sin(angle)
                
                
                body2.ax += a2*math.cos(angle + math.pi)
                body2.ay += a2*math.sin(angle + math.pi)
                
                
                #Sun.ax = force/Sun.mass*math.cos(angle+math.pi) #may need a plus pi? #not sure why this one needs to be negative??
                #Sun.ay = force/Sun.mass*math.sin(angle+math.pi) #may need a plus pi?
        
                #print('Sun a: ', Sun.ax, Sun.ay)
                #print(Sun.ay)

                #Earth.ax = force/Earth.mass*math.cos(angle) 
                #Earth.ay = force/Earth.mass*math.sin(angle)

                #print('Earth acceleration:', Earth.ax, Earth.ay)
        temp_list = []
        for body in solar_system:
            #print(body.x, body.ax)
            #print(body.y, body.ay)
            body.update_position(dt)
            body.update_velocity(dt)
            body.reset_acceleration()
            temp_list.append(body.x)
            temp_list.append(body.y)

        pos_history.append(temp_list)

    return solar_system, pos_history, times


def numpy_sim(solar_system, iters, init_time):
    print("Running numpy simulation...")
    #first take the solar system object then create numpy arrays to use for the sim
    
    #(x,y) for each body
    pos = np.zeros((len(solar_system), 2))
    vel = np.zeros((len(solar_system), 2))
    mass = np.zeros(len(solar_system))

    time_checks = []
    times = []
    #no good atm 
    #needs to be changed
    #may be better for this to be passed in
    for i in range(1, 5):
        time_checks.append(int(iters/5*i))


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
    
    pos_history = np.zeros((iters, 2*len(solar_system)))

    for i in range(iters):

        if i in time_checks:
           times.append(time.perf_counter()-init_time) 
        


        acc = compute_a(pos, mass)
        pos += vel*dt
        vel += acc*dt

        past_x[i] = pos[:,0]
        past_y[i] = pos[:,1]
        pos_history[i] = pos.flatten()

    

    #updates the original object and returns that!

    for i in range(len(solar_system)):
        solar_system[i].x = pos[i][0]
        solar_system[i].y = pos[i][1]
        solar_system[i].vx = vel[i][0]
        solar_system[i].vy = vel[i][1]
        solar_system[i].x_positions = past_x[:,i]
        solar_system[i].y_positions = past_y[:,i]


    return solar_system, pos_history, times

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

