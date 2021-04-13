#only gets the planet coords if they don't already exist
#assumes they wont be changed often!
if test ! -f "source/planet_coordinates.txt"; then
    eval python3 source/get_planet_coords.py
fi

#want to add in conditions to maybe delete resutls folder
#maybe to make sure the directory exists for now:

#start mucking around with deleting stuff once I have a git backup lol!

#currently all the files need the path into the files which is very messy
#need a better way of storing the path to the files
#maybe have some base $path variable like amrex!
eval python3 source/basic_python_sim.py

eval python3 source/plot_trajectories.py
