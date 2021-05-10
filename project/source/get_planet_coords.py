#NEEDS WORK
from astroquery.jplhorizons import Horizons
import numpy as np

import sys


flag = sys.argv[1]


#conversions to get units in better forms
kg_to_SM = 5.02785*10**(-31)
#km_to_AU = 6.68459*10**(-9)


#corresponds to March 19 2021
epoch = 2459293.33546


planet_coord_file = 'planet_coords.txt'

bodies = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']


#could just have a list of the masses??


body_properties = {'Sun': (1.988e30, 6.955e5),
            'Mercury': (3.301e23, 2440.),
            'Venus': (4.867e+24, 6052.),
            'Earth': (5.972e24, 6371.),
            'Mars': (6.417e23, 3390.),
            'Jupiter': (1.899e27, 69911.),
            'Saturn': (5.685e26, 58232.),
            'Uranus': (8.682e25, 25362.),
            'Neptune': (1.024e26, 24622.)
           }



#consider the 'real' simulation of 9 plents and 1 asteroid!
if flag == 'Real':
    
    bodies_to_query = 9
    #output_file = 'source/' + planet_coord_file
    output_file = 'source/real_planet_coords.txt'



    with open(output_file, 'w') as f:
        
        for i in range(bodies_to_query):
            query = Horizons(id=i, location='@sun', epochs=epoch, id_type='id').vectors()
            #formating could do with some work!
            f.write('{} {} {} {} {} \n'.format(query['x'].data[0], query['y'].data[0], query['vx'].data[0], 
                   query['vy'].data[0],  body_properties[bodies[i]][0]*kg_to_SM))

else:
    #this will need to be scaled big time!
    output_file = 'source/fake_planet_coords.txt'
    bodies = argv[2]
    coords = np.random.rand(bodies, 5)
    #set all masses to 1
    coords[:,4] = 1
    #this might not be saving in correct form!
    np.savetxt(output_file, coords)

