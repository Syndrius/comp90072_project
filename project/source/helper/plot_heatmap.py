#Written by Matthew Thomas 831343, May 2021 for COMP90072 at unimelb

#This file plots the heatmaps shown in the report


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

with open('source/data/heatmap.txt', 'r') as f:
    lines = f.readlines()


#plotting the heatmap!
cb = []
cm = []
pn = []
pm = []
labels = []
lines2 = []
    
#extracts the proper lines for each method
cb = lines[::5]
cm = lines[1::5]

pn = lines[2::5]
pm = lines[3::5]

labels = lines[4::5]

#should always be an integer!
size = int(np.sqrt(len(cm)))

cb_n = np.zeros((size, size))
cm_n = np.zeros((size, size))
pn_n = np.zeros((size, size))
pm_n = np.zeros((size, size))

x_labs = []
y_labs = []

k = 0
#creates the arrays for plotting
for i in range(size):
    for j in range(size):
        cb_n[j][i] = cb[k].split()[-2]
        cm_n[j][i] = cm[k].split()[-2]
        pn_n[j][i] = pn[k].split()[-2]
        pm_n[j][i] = pm[k].split()[-2]
        y_labs.append(int(labels[k].split()[0]))
        x_labs.append(int(labels[k].split()[1]))
        k += 1
        
x_labs = sorted(set(x_labs))
y_labs = sorted(set(y_labs))

#normalise data!
#'''
for i in range(size):
    for j in range(size):
        norm = np.max([cb_n[i][j], cm_n[i][j], pn_n[i][j], pm_n[i][j]])
        cb_n[i][j] = cb_n[i][j]/norm
        cm_n[i][j] = cm_n[i][j]/norm
        pn_n[i][j] = pn_n[i][j]/norm
        pm_n[i][j] = pm_n[i][j]/norm
#'''   
        
fig, ax = plt.subplots(2, 2)




sns.heatmap(cb_n, ax = ax[0][0], xticklabels=x_labs, yticklabels=y_labs, vmin=0, vmax=1, cmap='Reds')
sns.heatmap(cm_n, ax = ax[0][1], xticklabels=x_labs, yticklabels=y_labs, vmin=0, vmax=1, cmap='Oranges')
sns.heatmap(pn_n, ax = ax[1][0], xticklabels=x_labs, yticklabels=y_labs, vmin=0, vmax=1, cmap='Blues')
sns.heatmap(pm_n, ax = ax[1][1], xticklabels=x_labs, yticklabels=y_labs, vmin=0, vmax=1, cmap='Purples')
ax[1][0].set_xlabel('Timesteps')
ax[0][0].set_ylabel('Bodies')

ax[1][0].set_ylabel('Bodies')
ax[1][1].set_xlabel('Timesteps')

ax[0][0].set_title("Basic C")
ax[0][1].set_title("Multi C")
ax[1][0].set_title("Numpy")
ax[1][1].set_title("Multi Py")

ax[0][0].set_yticklabels(ax[0][0].get_yticklabels(), rotation=0)
ax[0][1].set_yticklabels(ax[0][1].get_yticklabels(), rotation=0)
ax[1][0].set_yticklabels(ax[1][0].get_yticklabels(), rotation=0)
ax[1][1].set_yticklabels(ax[1][1].get_yticklabels(), rotation=0)
plt.tight_layout()
plt.savefig("results/heatmaps.png")
plt.show()


#plots the fastest and slowest method

fastest = np.zeros((size, size))
slowest = np.zeros((size, size))

for i in range(size):
    for j in range(size):
        max_ind = np.argmax([cb_n[i][j], cm_n[i][j], pn_n[i][j], pm_n[i][j]])
        min_ind = np.argmin([cb_n[i][j], cm_n[i][j], pn_n[i][j], pm_n[i][j]])
        if max_ind == 0:
            slowest[i][j] = 1
        elif max_ind == 1:
            slowest[i][j] = 2
        elif max_ind == 2:
            slowest[i][j] = 3
        else:
            slowest[i][j] = 4

        if min_ind == 0:
            fastest[i][j] = 1
        elif min_ind == 1:
            fastest[i][j] = 2
        elif min_ind == 2:
            fastest[i][j] = 3
        else:
            fastest[i][j] = 4


new_y_labs = sorted(set(y_labs))
new_x_labs = sorted(set(x_labs))


myColors = ['darkred', 'darkorange', 'royalblue', 'orchid']
cmap = LinearSegmentedColormap.from_list('Custom', myColors, len(myColors))

ax = sns.heatmap(fastest, cmap=cmap, xticklabels=new_x_labs, yticklabels=new_y_labs, linewidths=.5, linecolor='lightgray')
colorbar = ax.collections[0].colorbar
colorbar.set_ticks([1.4, 2.1, 2.9, 3.6])
colorbar.set_ticklabels(['Basic C', 'Multi C', 'Numpy', 'Multi Py'])
ax.set_xlabel('Timesteps')
ax.set_ylabel('Bodies')
ax.set_title("Fastest Implementation")
plt.savefig("results/fastest_heatmap.png")
plt.show()
ax = sns.heatmap(slowest, cmap=cmap, xticklabels=new_x_labs, yticklabels=new_y_labs, linewidths=.5, linecolor='lightgray')
colorbar = ax.collections[0].colorbar
colorbar.set_ticks([1.4, 2.1, 2.9, 3.6])
colorbar.set_ticklabels(['Basic C', 'Multi C', 'Numpy', 'Multi Py'])
ax.set_xlabel('Timesteps')
ax.set_ylabel('Bodies')
ax.set_title("Slowest Implementation")
plt.savefig("results/slowest_heatmap.png")
plt.show()
