from astroquery.jplhorizons import Horizons

#want to get this info from somewhere else!
num_planets = 8
#corresponds to March 19 2021
epoch = 2459293.33546

#conversions to get units in better forms
kg_to_SM = 5.02785*10**(-31)
km_to_AU = 6.68459*10**(-9)

output_file = 'planet_coordinates.txt'

#needs to be redone in a better way!
#probably want the asteroid here too!
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
bodies = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

with open(output_file, 'w') as f:
    
    #+1 to include the sun!
    for i in range(num_planets+1):
        query = Horizons(id=i, location='@sun', epochs=2459293.33546, id_type='id').vectors()
        #formating could do with some work!
        f.write('{} {} {} {} {} {} \n'.format(query['x'].data[0], query['y'].data[0], query['vx'].data[0], 
               query['vy'].data[0], body_properties[bodies[i]][1]*km_to_AU, body_properties[bodies[i]][0]*kg_to_SM))
