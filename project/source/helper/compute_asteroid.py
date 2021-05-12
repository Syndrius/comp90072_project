
#this file works as intended atm
#This file finds the initial coordiantes of an asteroid that will collide with Earth
#It runs the simulation, then creates and asteroid at Earths location, then runs
#the sim backwards to get the asteroids initial conditions.


import math #dont think this is needed!
#import csv #dont think this is required
#import python_sims 
import sys
import numpy as np

#need to stop defining these everywhere
G = 2.96*10**(-4)
dt = 0.01

#reads the command line arguements to get the file to use and the number of iterations
coord_file = sys.argv[1]
iters = int(sys.argv[2])


#basic version of the numpy sim 
def sim(ss, iters):

    for i in range(iters):

        #gets the acceleration of each body
        ax, ay = compute_a(ss)
        #updates the x and y of each body
        ss[0] += ss[2]*dt
        ss[1] += ss[3]*dt
        #updates the vx and vy of each body
        ss[2] += ax*dt
        ss[3] += ay*dt

    return ss

#computes the acceleration of each body for the sim function
def compute_a(ss):

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
    
    ax = -G * (dx * inv_dist_cubed) @ mass
    ay = -G * (dy * inv_dist_cubed) @ mass

    return ax, ay


#reads the initial coordinates of the other planets
ss = np.loadtxt(coord_file).T


#runs the simulation once, to find the 'final positions' of the bodies
ss = sim(ss, iters)

   
#reverses the direction of the bodies in the solar system
#so the simulation can be run backwards!
ss[2] =-ss[2]
ss[3] =-ss[3]


#creates a larger ss so the asteroid can fit, and adds the old values in
ss_ast = np.zeros((ss.shape[0], ss.shape[1]+1))

for i in range(5):
    ss_ast[i][:-1] = ss[i]


#add the asteroid in
#slightly offset asteroid from earth to prevent overflow
ss_ast[0][-1] = ss[0][3] + 0.00085 #sets x pos as same as Earths
ss_ast[1][-1] = ss[1][3] + 0.00085 #sets y coord
#random velcity for ast
ss_ast[2][-1] = 0.025
ss_ast[3][-1] = - 0.008

#sets mass to be very low, such that the asteroid wont have any effect on the other planets
ss_ast[4][-1] = 10**(-20)


#runs the sim backwards 
ss = sim(ss_ast, iters)

#reverses the asteroid trajectory so that it will be heading towards Earth
ss_ast[2][-1] = -ss_ast[2][-1]
ss_ast[3][-1] = -ss_ast[3][-1]

#appends the asteroids initial coordinates to the file
with open(coord_file, 'a') as f:
    np.savetxt(f, ss_ast[:,-1], newline=" ")

