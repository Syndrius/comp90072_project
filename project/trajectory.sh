#Written by Matthew Thomas 831343, May 2021 for COMP90072 at unimelb

#main file that controls which simulation and scenarios are run
#calls the coordinate generation, the simulations and the plotting files

#reads the inputs
source inputs

#empty strings for adding flags to be passed around to!
PY_FLAGS=""
C_FLAGS=""


DATA_DIR="source/data"

#creates the directories if they don't exist
if [ ! -e $DATA_DIR ]; then
    eval mkdir source/data
fi

if [ ! -e "results" ]; then
    eval mkdir results
fi


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



#Runs the c simulations with appropriate flags
run_c_sims () {
    if [ -n "$C_FLAGS" ]; then
        if [ ! -f "source/c_sim" ]; then
            echo "Compiling c simulations:"
            eval gcc-6 -fopenmp -Wall -o c_sim source/c_sims/main.c source/c_sims/sims.c source/c_sims/helper.c
            eval mv c_sim source/
            echo "Done"
        fi
        echo "Running c simulations:"
        eval ./source/c_sim $FLAGS $NUM_BODIES $C_FLAGS
        echo "Finished c simulations."
    fi

}
#Runs the python simulations with the appropriate flags
run_py_sims () {
    #ie only runs the python simulation if one of the sims is being called!
    if [ -n "$PY_FLAGS" ]; then
        echo "Running python simulations:"
        eval python3 source/py_sims/main.py $FLAGS $PY_FLAGS
        echo "Finished python simulations."
    fi
}


#If true, runs the simulations with the initial coordinates of the real planets
if [ $REAL = true ]; then
    ITERS=500000
    NUM_BODIES=10
    INITIAL_COORD_FILE="source/helper/real_planet_coords.txt"
    FLAGS="$INITIAL_COORD_FILE $ITERS"
    #gets the initial coord file then generates the asteroid
    if [ ! -f $INITIAL_COORD_FILE ]; then
        eval python3 source/helper/get_planet_coords.py "Real"
        eval python3 source/helper/compute_asteroid.py $FLAGS
    fi
    #runs the sims
    run_c_sims
    run_py_sims
    eval rm source/c_sim
    #plots the trajectories and the time taken
    eval python3 source/helper/plot_trajectories.py
    eval python3 -W ignore source/helper/plot_times.py
    eval rm source/data/time.txt

#Creates heatmaps comparing the methods for different numbers of bodies and timesteps
elif [ $HEATMAP = true ]; then
    INITIAL_COORD_FILE="source/helper/fake_planet_coords.txt"
    iters=(50 100 300 1000 2000)
    bodies=(10 100 300 500 1000)
    #heatmap always excludes basic py and includes everything else
    PY_FLAGS="n m"
    C_FLAGS="b m"
    for i in ${iters[@]}; do
        for j in ${bodies[@]}; do
            echo "Iters " $i "bodies " $j
            ITERS=$i
            NUM_BODIES=$j
            FLAGS="$INITIAL_COORD_FILE $ITERS"
            eval python3 source/helper/get_planet_coords.py "Fake" $NUM_BODIES
            run_c_sims
            run_py_sims
            echo "$NUM_BODIES $ITERS " >> source/data/time.txt

        done
    done
    eval mv source/data/time.txt source/data/heatmap.txt
    eval python3 source/helper/plot_heatmap.py
    eval rm source/c_sim

#otherwise run the sim with the generated bodies
else
    INITIAL_COORD_FILE="source/helper/fake_planet_coords.txt"
    FLAGS="$INITIAL_COORD_FILE $ITERS"
    eval python3 source/helper/get_planet_coords.py "Fake" $NUM_BODIES
    run_c_sims
    run_py_sims
    eval rm source/c_sim
    eval python3 -W ignore source/helper/plot_times.py
    eval rm source/data/time.txt
fi

