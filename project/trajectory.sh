#NEEDS WORK

#TODO
#add gpu for python -> looks like this will be harder than initial thought, maybe give it a go later?, may be easier on ubuntu??
#
#tidy up plotting
#
#write a little author and description thing for each file
#
#README file!

source inputs

#may want to convert strings to lower etc for generic input

#empty strings for adding flags to be passed around to!
PY_FLAGS=""
C_FLAGS=""

#can do this over a loop to see how they run with variable number of bodies!
#or just manually run it a few times and save the output files!
NUM_BODIES=1000

RESULTS_DIR="source/results"

#this determines what type of initial coords are generated!
if [ $REAL = true ]; then
    #want to be able to choose this/have two options depending on real planets or fake
    ITERS=500000
    INITIAL_COORD_FILE="source/helper/real_planet_coords.txt"
    #needed for c
    NUM_BODIES=10
    FLAGS="$INITIAL_COORD_FILE $ITERS"
    #gets the initial coord file then generates the asteroid!
    if [ ! -f $INITIAL_COORD_FILE ]; then
        eval python3 source/helper/get_planet_coords.py "Real"
        eval python3 source/helper/compute_asteroid.py $FLAGS
    fi
else
    #probably want to consider 3 cases:
    #the real, ~loads of bodies and barely any iters
    #somewhere in between
    ITERS=100
    INITIAL_COORD_FILE="source/helper/fake_planet_coords.txt"
    FLAGS="$INITIAL_COORD_FILE $ITERS"
    if [ ! -f $INITIAL_COORD_FILE ]; then
        eval python3 source/helper/get_planet_coords.py "Fake" $NUM_BODIES
    fi
fi

#can check size of coord file to see if it needs to be remade
#probabaly have plot_traj always false unless real=true

#adds the appropriate flags for each sim
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

if [ $MULTI_C_SIM = true ]; then
    C_FLAGS="$C_FLAGS m"
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
    eval python3 source/py_sims/main.py $FLAGS $PY_FLAGS
    echo "Finished python simulations."
fi

#maybe shouldn't compile everytime??
#maybe run c before python if multi c is wrong!
if [ -n "$C_FLAGS" ]; then
    echo "Compiling c simulations:"
    #maybe define varibles of compiler and flags etc
    #may want to split the compiling of multi and base up!
    #need to determine best place to put exe
    #think where it is, is good, as interactions with results dir wont change
    eval gcc-6 -fopenmp -Wall -o c_sim source/c_sims/main.c source/c_sims/sims.c source/c_sims/helper.c
    #this is to ensure file are in right spot and can read other files!
    eval mv c_sim source/
    echo "Done"
    echo "Running c simulations:"
    eval ./source/c_sim $FLAGS $NUM_BODIES $C_FLAGS
    echo "Finished c simulations."
fi

#maybe need a guard to check the results directory isn't empty!
if [ $PLOT_TRAJ = true ]; then
    #checks there are some results to plot
    if [ ! -f $RESULTS_DIR"/data.txt" ]; then
        echo "No data found, please run one of the simulations."
    else
        echo "Plotting the trajectories..."
        eval python3 source/helper/plot_trajectories.py
        echo "Done"
    fi
fi

#should add similar guard as plot_traj
if [ $PLOT_TIMES = true ]; then
    eval python3 source/helper/plot_times.py
fi
