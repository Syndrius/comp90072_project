# Written by Matthew Thomas 831343, May 2021 for COMP90072 at unimelb

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.ticker import AutoLocator, AutoMinorLocator

input_file = "source/data/time.txt"

#dictionary that stores the labels and colours for each sim
dict_labels = {'pb':'Basic Python', 'pn':"Numpy", 'cb':"Basic C", 'pm': 'Python Multi', 'cm': 'C Multi'}
dict_colours = {'pb':'limegreen', 'pn':"royalblue", 'cb':"red", 'pm': 'magenta', 'cm': 'darkorange'}


data = []
labels = []
max_time = 0
with open(input_file, 'r') as f:
    
    #each line is a string
    for line in f:
        line_list = line.split()
        label = line_list[-1]
        line_data = [float(i) for i in line_list[:-2]]
        data.append(line_data)
        labels.append(line_list[-1])
       

#need the placeholder as matplotlib has a hidden tick
x_axis_labels = ["placehoder", "0%", "20%", "40%", "60%", "80%", "100%"]

fig, ax = plt.subplots()

#plots the data
for i in range(len(data)):
    ax.plot(data[i], label=f"{dict_labels[labels[i]]}: {data[i][-1]:.2f}s", color=dict_colours[labels[i]])


ax.yaxis.set_major_locator(AutoLocator())
ax.xaxis.set_major_formatter('{x:.0f}')

ax.set_xticklabels(x_axis_labels, rotation=0)
plt.legend(loc="upper left")

plt.xlabel("Timesteps Complete")

plt.ylabel("Time (s)")

ax.yaxis.set_minor_locator(AutoMinorLocator())
plt.savefig("results/simulation_time.png")
plt.show()

