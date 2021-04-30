#this file's purpose is unclear atm, different files are reading different things from this 
#really dont like this file! -> bash should probably pass this around I think!


num_bodies = 10
bodies_to_query = 9



#conversions to get units in better forms
kg_to_SM = 5.02785*10**(-31)
km_to_AU = 6.68459*10**(-9)


#corresponds to March 19 2021
epoch = 2459293.33546


planet_coord_file = 'planet_coords.txt'

bodies = ['Sun', 'Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']


#THIS IS STUPID, WHY STORE MASSES IN UNITS THAT DON"T WORK!
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

G = 2.96 *10**(-4) #units of Au^3/solar_mass/days^2

#timestep!
dt = 0.01


iters = 500000


#will need to contain a list of files for the results to be written to, bash may
#need to make this happen!
