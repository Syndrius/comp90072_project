#NEEDS WORK

#TODO
#implement read and write for different types
#may have to ignore file reading and writing for Multi
#
#Fix base c alg for new ss structure -> files will need to be read differently
#
#add multiprocessing for c
#
#add gpu for python
#
#tidy up plotting
#
#clean up all the funcs

source inputs

#may want to convert strings to lower etc for generic input

#currently:
#c ~10s
#numpy ~30s
#base_python ~80s


#empty strings for adding flags to be passed around to!
PY_FLAGS=""
C_FLAGS=""

#can do this over a loop to see how they run with variable number of bodies!
NUM_BODIES=1000

RESULTS_DIR="source/results"

#this determines what type of initial coords are generated!
if [ $REAL = true ]; then
    #want to be able to choose this/have two options depending on real planets or fake
    ITERS=500000
    INITIAL_COORD_FILE="source/real_planet_coords.txt"
    #needed for c
    NUM_BODIES=10
    FLAGS="$INITIAL_COORD_FILE $ITERS"
    #gets the initial coord file then generates the asteroid!
    if [ ! -f $INITIAL_COORD_FILE ]; then
        eval python3 source/get_planet_coords.py "Real"
        eval python3 source/compute_asteroid.py $FLAGS
    fi
else
    #probably want to consider 3 cases:
    #the real, ~loads of bodies and barely any iters
    #somewhere in between
    ITERS=100
    INITIAL_COORD_FILE="source/fake_planet_coords.txt"
    FLAGS="$INITIAL_COORD_FILE $ITERS"
    if [ ! -f $INITIAL_COORD_FILE ]; then
        eval python3 source/get_planet_coords.py "Fake" $NUM_BODIES
    fi
fi

#can check size of coord file to see if it needs to be remade
#probabaly have plot_traj always false unless real=true

if [ $BASE_PY_SIM = true ]; then
    PY_FLAGS="$PY_FLAGS b"
fi

if [ $NUMPY_SIM = true ]; then
    PY_FLAGS="$PY_FLAGS n"
fi

if [ $MULTI_PY_SIM = true ]; then
    PY_FLAGS="$PY_FLAGS m"
fi


if [ $BASE_C_SIM = true ]; then
    C_FLAGS="$C_FLAGS b"
fi

#wont always want to do this, but good for now!
eval rm source/results/time.txt

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


#creates the results directory if it does not exist!
#this should probably have the RESULT_DIR variable
if [ ! -e 'source/results' ]; then
    eval mkdir source/results
fi

#string is not empty
#ie only runs the python simulation if one of the sims is being called!
if [ -n "$PY_FLAGS" ]; then
    echo "Running python simulations:"
    eval python3 source/python_main.py $FLAGS $PY_FLAGS
    echo "Finished python simulations."
fi


#maybe shouldn't compile everytime??
if [ -n "$C_FLAGS" ]; then
    echo "Compiling c simulations:"
    #maybe define varibles of compiler and flags etc
    eval gcc -Wall -o c_sim source/c_main.c source/c_sims.c
    #this is to ensure file are in right spot and can read other files!
    eval mv c_sim source/
    echo "Done"
    echo "Running basic c simulations..."
    eval ./source/c_sim $FLAGS $NUM_BODIES $C_FLAGS
    echo "Finished c simulations."
fi

#not sure if i need to consider plotting different methods
#they should all result in the same file of numbers!
#need to pass command line argument with the file in it!
#maybe need a guard to check the results directory isn't empty!
if [ $PLOT_TRAJ = true ]; then
    #checks there are some results to plot
    if [ ! -f $RESULTS_DIR"/data.txt" ]; then
        echo "No data found, please run one of the simulations."
    else
        echo "Plotting the trajectories..."
        eval python3 source/plot_trajectories.py
        echo "Done"
    fi
fi


if [ $PLOT_TIMES = true ]; then
    eval python3 source/plot_times.py
fi
