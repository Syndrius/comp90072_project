#echo $1
source inputs
#echo $BASE_PY
#echo $NUM_PLANETS

#may want some generic path variable that is just 'source/'

#only gets the planet coords if they don't already exist
#assumes they wont be changed often!
#file name shouldn't be written here, this will need acces to constants
#structure may have to change once c comes into it!
if test ! -f "source/planet_coords.txt"; then
    eval python3 source/get_planet_coords.py
fi

num_lines=$(< "source/planet_coords.txt" wc -l)

#define the file golly gosh!
#if the file only has 9 lines, the asteroid needs to be added
if test $num_lines -eq 9; then
   eval python3 source/compute_asteroid.py
fi

#want to add in conditions to maybe delete resutls folder
#maybe to make sure the directory exists for now:

#start mucking around with deleting stuff once I have a git backup lol!

#currently all the files need the path into the files which is very messy
#need a better way of storing the path to the files
#maybe have some base $path variable like amrex!
#creates the results directory if it does not exist!
if test ! -e 'source/results'; then
    eval mkdir source/results
fi

#eval python3 source/basic_python_sim.py

#eval python3 source/plot_trajectories.py
