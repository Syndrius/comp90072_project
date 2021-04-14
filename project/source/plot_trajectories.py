import numpy as np
import matplotlib.pyplot as plt
from constants import *



#will need a list of this, for each file, think the bash script needs to create this files!
coord_file_base = 'source/results/data_body_'


for i in range(num_bodies):
    input_file_str = coord_file_base + str(i) + '.txt'
    #x = []
    #y = []
    #input_file = open(input_file_str, 'r')
    x, y = np.loadtxt(input_file_str, delimiter=' ', unpack=True)
    #with open(input_file_str, 'r') as filein:
        #reader = csv.reader(filein, delimiter=' ')
        #print(*reader)
        #print(list(zip(*reader)))
        #x, y = zip(*reader)
        #print(x)
        #print(y)
    plt.plot(x, y)
    #input_file = open(input_file_str, 'r')

plt.show()
