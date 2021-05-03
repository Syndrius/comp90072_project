#placeholder, plots the time taken for each simulation.
#may want to combine with the other plotting file later

#works well enough, may want to change colours
#need to add the other sims as they are added

#may want to make the scale more adjustable, ie based on max

#gotta stop importing all this everywhere!
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

#may need a /source in here when calling from bash
input_file = "source/results/time.txt"

#numpy cant be used here!
#data = np.loadtxt(input_file)


#dictionary that stores the labels for each sim
#labels and names will change
dict_labels = {'pb':'Basic Python', 'pn':"Numpy", 'c':"Basic C"}


data = []
labels = []
with open(input_file, 'r') as f:
    
    #each line is a string
    for line in f:
        line_list = line.split()
        label = line_list[-1]
        line_data = [float(i) for i in line_list[:-1]]
        data.append(line_data)
        labels.append(line_list[-1])
        

#print(labels)
#print(data)

#need the placeholder as matplotlib think a hidden tick is a good idea!
x_axis_labels = ["placehoder", "Start", "Data In", "1/5", "2/5", "3/5", "4/5", "Sim Done", "Data Out"]

fig, ax = plt.subplots()

#probably want to do this as two figures, one with basic python, and one without
for i in range(len(data)):

    ax.plot(data[i], label=dict_labels[labels[i]])


#may need a warning suppresion fir this fixed locator nonsense


#print(data[0])
#plt.plot(data[0])
#ticks_loc = ax.get_yticks().tolist()
#ax.set_yticks(mticker.FixedLocator(ticks_loc))
#plt.xticks(ticks=np.arange(len(data[0])), labels=x_axis_labels)
#plt.yticks(np.arange(0, 70, 0.5))
ax.yaxis.set_major_locator(MultipleLocator(5))
#ax.yaxis.set_major_formatter('{x:.0f}')

ax.set_xticklabels(x_axis_labels, rotation=45)
#need to be careful with plt vs ax vs fig
plt.legend(loc="upper left")

plt.title("Simulation Time")

plt.ylabel("Time (s)")

# For the minor ticks, use no labels; default NullFormatter.
ax.yaxis.set_minor_locator(MultipleLocator(1))
plt.show()

