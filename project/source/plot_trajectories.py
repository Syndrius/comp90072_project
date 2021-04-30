#this file is quite slow, probably because of the large file reading??
#but shouldn't need to be called much so doesn't matter
#takes ~ 1min
#new plotting method works for python, need to change c!

#not sure if this should do all of the plotting!
#could just pass command line args again
#probably dont want to create too many more files!
#create one for now, and can combine them later!

#TODO
#add planets to ends of plots
#make this work for different amount of bodies
#clean up


import numpy as np
import matplotlib.pyplot as plt
from constants import *
from matplotlib import colors



#will need a list of this, for each file, think the bash script needs to create this files!
coord_file_base = 'source/results/data_body_'

#only one file for now, may want to change the name!
input_file = "source/results/data.txt"

#colours for Sun, mercury, venus, earth, mars, jupiter, saturn, neptune, uranus, asteroid
colours = ['darkorange', 'grey', 'linen', 'forestgreen', 'red', 'wheat', 'goldenrod', 'lightcyan', 'royalblue', 'sienna']


#need .T because it reads it in a stupid way!
data = np.loadtxt(input_file, delimiter=' ').T

#will need to be very careful with the num_bodies here, its purpose
#as a constant is not super clear!
#dont like this itterable, not adjustable for more bods
for i in range(num_bodies):
    #input_file_str = coord_file_base + str(i) + '.txt'
    #x = []
    #y = []
    #input_file = open(input_file_str, 'r')
    #x, y = np.loadtxt(input_file_str, delimiter=' ', unpack=True)
    x = data[2*i]
    y = data[2*i+1]
    #with open(input_file_str, 'r') as filein:
        #reader = csv.reader(filein, delimiter=' ')
        #print(*reader)
        #print(list(zip(*reader)))
        #x, y = zip(*reader)
        #print(x)
        #print(y)
    #this doesn't work, but should work in newer versions of matplotlib!
    #alphas = np.linspace(0, 1, len(x))
    #alphas[:len(x)/2] = 0
    num = len(x)
    #cmap = colors.LinearSegmentedColormap.from_list(
    #    'incr_alpha', [(0, (*colors.to_rgb(colours[i]),0)), (1, colours[i])])
    #this doesn't work as different planets sweep different amounts
    #some will have gaps, some will have bright spots!
    #try not segmenting this instead!
    #THIS IS THE WAY!
    #plot it all first at low transparency
    plt.plot(x, y, alpha=0.1, color=colours[i])
    val = 400000
    al = 0.02
    #looks pretty good, maybe could be brighter at the ends

    #also want to add spheres to end
    #also plot two figures with different zooms
    while al < 0.95:
            
        plt.plot(x[val:], y[val:], alpha=al, color=colours[i])
        val += 10000
        al += 0.01
    #first plot the entire thing on a low transparancy
    #plt.plot(x, y, color=colours[i], alpha=0.1)
    #input_file = open(input_file_str, 'r')

#should have both the zoomed in one and the large one with subplots
ax = plt.gca()
ax.set_facecolor('black')
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.show()
