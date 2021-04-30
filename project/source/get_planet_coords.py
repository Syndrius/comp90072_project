#this file is probably fine, is quite pointless
from astroquery.jplhorizons import Horizons
from constants import * 

output_file = 'source/' + planet_coord_file

with open(output_file, 'w') as f:
    
    for i in range(bodies_to_query):
        query = Horizons(id=i, location='@sun', epochs=2459293.33546, id_type='id').vectors()
        #formating could do with some work!
        f.write('{} {} {} {} {} {} \n'.format(query['x'].data[0], query['y'].data[0], query['vx'].data[0], 
               query['vy'].data[0], body_properties[bodies[i]][1]*km_to_AU, body_properties[bodies[i]][0]*kg_to_SM))
