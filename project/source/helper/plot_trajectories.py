# Written by Matthew Thomas 831343, May 2021 for COMP90072 at unimelb

#plots the trajectories of the planets

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


input_file = "source/data/data.txt"

#colours for Sun, mercury, venus, earth, mars, jupiter, saturn, neptune, uranus, asteroid
colours = ['darkorange', 'grey', 'linen', 'forestgreen', 'firebrick', 'khaki', 'goldenrod', 'turquoise', 'royalblue', 'sandybrown']
bodies = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Asteroid']
size = [0.25, 0.01, 0.05, 0.05, 0.01, 0.1, 0.1, 0.15, 0.15, 0.01]

#need .T to ensure data is in correct form
data = np.loadtxt(input_file, delimiter=' ').T

fig, ax = plt.subplots(1, 2)

for i in range(int(data.shape[0]/2)):
    x = data[2*i]
    y = data[2*i+1]
    num = len(x)

    #this plots at variable transparencies to get fade effect
    ax[0].plot(x, y, alpha=0.1, color=colours[i])
    ax[1].plot(x, y, alpha=0.1, color=colours[i])
    val = 400000
    al = 0.02
    while al < 0.95:
           
        ax[0].plot(x[val:], y[val:], alpha=al, color=colours[i])
        ax[1].plot(x[val:], y[val:], alpha=al, color=colours[i])
        val += 10000
        al += 0.01

    #adds circles at end to represent planets
    planet1 = plt.Circle((x[-1], y[-1]), size[i], color=colours[i])
    planet2 = plt.Circle((x[-1], y[-1]), size[i], color=colours[i])
    ax[0].add_patch(planet1)
    ax[1].add_patch(planet2)

#plots the trajectories for different zooms
ax[0].set_facecolor('black')
ax[1].set_facecolor('black')
ax[1].set_xlim(-3, 3)
ax[1].set_ylim(-3, 3)
ax[0].set_ylim(-10, 25)
ax[0].tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
ax[1].tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
plt.savefig("results/trajectories.png")
plt.show()
