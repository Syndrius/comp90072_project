#echo $1
source inputs
#echo $BASE_PY
#echo $NUM_PLANETS

#currently:
#c ~10s
#numpy ~30s
#base_python ~80s

INITIAL_COORD_FILE="source/planet_coords.txt"
RESULTS_DIR="source/results"


#may want some generic path variable that is just 'source/'

#only gets the planet coords if they don't already exist
#assumes they wont be changed often!
#file name shouldn't be written here, this will need acces to constants
#structure may have to change once c comes into it!
#maybe should pass the file name in as a command line argument
if [ ! -f $INITIAL_COORD_FILE ]; then
    eval python3 source/get_planet_coords.py
fi

num_lines=$(< $INITIAL_COORD_FILE wc -l)

#define the file golly gosh!
#if the file only has 9 lines, the asteroid needs to be added
#if the file only has the initial bodies adds the asteroid to it
if [ $num_lines -eq $INITIAL_BODIES ]; then
    #this file should be improved with numpy etc
   echo "Computing the asteroids initial conditions..."
   eval python3 source/compute_asteroid.py
fi

#want to add in conditions to maybe delete resutls folder
#maybe to make sure the directory exists for now:
#this should be earlier in the file, won't be using this much
#more a proof of concept for final code
#probably want to delete the c files as well
if [ $CLEAN = true ]; then
    echo "clean up dawg"
    #deletes the results folder
    eval rm -r source/results
    #leave below commented out as recreating the coords is tiresome
    #eval rm source/planet_coords.txt
fi

#start mucking around with deleting stuff once I have a git backup lol!

#currently all the files need the path into the files which is very messy
#need a better way of storing the path to the files
#maybe have some base $path variable like amrex!
#creates the results directory if it does not exist!
if [ ! -e 'source/results' ]; then
    eval mkdir source/results
fi

if [ $RUN_PY_SIM = true ]; then
    echo "Running basic python simulation..."
    eval python3 source/basic_python_sim.py
    echo "Done"
fi

if [ $RUN_C_SIM = true ]; then
    echo "Compiling basic c simulation..."
    #maybe define varibles of compiler and flags etc
    eval gcc -Wall -o basic_c_sim source/basic_c_sim.c
    eval mv basic_c_sim source/
    echo "Done"
    echo "Running basic c simulation..."
    eval ./source/basic_c_sim
    echo "Done"
fi

#not sure if i need to consider plotting different methods
#they should all result in the same file of numbers!
#need to pass command line argument with the file in it!
#maybe need a guard to check the results directory isn't empty!
if [ $PLOT_TRAJ = true ]; then
    #checks there are some results to plot
    if [ ! -f $RESULTS_DIR"/data_body_0.txt" ]; then
        echo "No data found, please run one of the simulations."
    else
        echo "Plotting the trajectories..."
        eval python3 source/plot_trajectories.py
        echo "Done"
    fi
fi
