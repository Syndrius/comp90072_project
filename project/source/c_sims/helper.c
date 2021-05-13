/*
 * File of helper function that provide file input/output and memory allocation
 *
 *
 *
 */
#include "main.h"

/* Writes the history of positions for each body to the output file for plotting */
void write_pos(char *output_file, long double **pos_history, int iters, int size) {
    FILE *fp;
    // first open in write mode to ensure the file is empty before writing data
    fp = fopen(output_file, "w");
    fclose(fp);
    fp = fopen(output_file, "a");

    // writes the data line by line
    for (int i=0;i<iters;i++) {
        for (int j=0;j<2*size;j++) {
            // prevents extra whitespace at the end of the line
            if (j==2*size-1) {
                fprintf(fp, "%.15Lf", pos_history[i][j]);
            }
            else {
                fprintf(fp, "%.15Lf ", pos_history[i][j]);
            }
        }
        fprintf(fp, "\n");
    }
    fclose(fp);
}

/* Writes the time taken for the simulations */
void write_time(char *time_file, timer_t *timer, char* label) {
    FILE *fp;
    //label tells which sim 
    fp = fopen(time_file, "a");
    for (int i=0;i<timer->recorded;i++) {
        fprintf(fp, "%f ", timer->times[i]/1000);
    }
    // Assigns the label for the simulation
    fprintf(fp, "%s\n", label);
    fclose(fp);
}


/* Runs the basic simulation, creates the required data structures and writes to file */
void run_base_sim(solar_system_t *ss) {
    timer_t timer;
    long double **pos_history;

    // Creates the array for storing the history of positions
    pos_history = malloc(ss->max_iters * sizeof(*pos_history));
    init_pos_history(pos_history, ss->max_iters, ss->max_bodies);
    

    // Initialises the timer object
    gettimeofday(&timer.start, NULL);
    timer.recorded = 0;
    timer.times[timer.recorded] = 0;
    timer.recorded += 1;

    // Runs the simulation
    base_simulation(ss, pos_history, &timer);

    // Records the time after the sim is complete
    gettimeofday(&timer.stop, NULL);
    timer.times[timer.recorded] = timedifference_msec(timer.start, timer.stop);
    timer.recorded += 1;

    // Writes the position history to file
    write_pos(OUTPUT_FILE, pos_history, ss->max_iters, ss->max_bodies);
    
    // Records time after file write
    gettimeofday(&timer.stop, NULL);
    timer.times[timer.recorded] = timedifference_msec(timer.start, timer.stop);
    timer.recorded += 1;

    // Writes the times to file
    write_time(TIME_FILE, &timer, "cb");

}


/* Runs the multiprocessing simulation, creates the required data structures and writes to file */
void run_multi_sim(solar_system_t *ss) {
    timer_t timer;
    long double **pos_history;

    // Creates the array for storing the history of positions
    pos_history = malloc(ss->max_iters * sizeof(*pos_history));
    init_pos_history(pos_history, ss->max_iters, ss->max_bodies);

    // Initialise the timer
    gettimeofday(&timer.start, NULL);
    timer.recorded = 0;
    timer.times[timer.recorded] = 0;
    timer.recorded += 1;

    // Run the simulation
    multi_simulation(ss, pos_history, &timer);

    // Records the time after the sim is complete
    gettimeofday(&timer.stop, NULL);
    timer.times[timer.recorded] = timedifference_msec(timer.start, timer.stop);
    timer.recorded += 1;

    // Writes the position history to file
    write_pos(OUTPUT_FILE, pos_history, ss->max_iters, ss->max_bodies);
    
    // Records time after file write
    gettimeofday(&timer.stop, NULL);
    timer.times[timer.recorded] = timedifference_msec(timer.start, timer.stop);
    timer.recorded += 1;

    // Writes the time to file
    write_time(TIME_FILE, &timer, "cm");

}

/* Allocates the memory for storing the position history */
void init_pos_history(long double **pos_history, int iters, int size) {

    for (int i=0;i<iters;i++) {
        // 2 for x and y coords
        pos_history[i] = malloc(2*size*sizeof(**pos_history));
    }
}

/* Reads the initial coordinates into the solar system object */
void read_solar_system(FILE *fp, solar_system_t *ss) {


    while (!feof(fp) && (ss->num_bodies < ss->max_bodies)) {
        fscanf(fp, "%Lf %Lf %Lf %Lf %Lf",
            &ss->x[ss->num_bodies],
            &ss->y[ss->num_bodies],
            &ss->vx[ss->num_bodies],
            &ss->vy[ss->num_bodies],
            &ss->mass[ss->num_bodies]);

        ss->num_bodies += 1;
    }
}


/* returns the time difference in milliseconds */
float timedifference_msec(struct timeval t0, struct timeval t1)
{
    return (t1.tv_sec - t0.tv_sec) * 1000.0f + (t1.tv_usec - t0.tv_usec) / 1000.0f;
}

/* Initialises the solar system object */
void init_ss(char *coord_file, solar_system_t *ss, int iters, int num_bodies) {
    FILE *fp;

    ss->num_bodies = 0;
    ss->iters_complete = 0;
    ss->max_iters = iters;
    ss->max_bodies = num_bodies;

    // creates the arrays for storing the positions etc
    ss->x = malloc(ss->max_bodies*sizeof(long double));
    ss->y = malloc(ss->max_bodies*sizeof(long double));
    ss->vx = malloc(ss->max_bodies*sizeof(long double));
    ss->vy = malloc(ss->max_bodies*sizeof(long double));
    ss->mass = malloc(ss->max_bodies*sizeof(long double));

    fp = fopen(coord_file, "r");
    
    
    //reads the initial coordinates into ss 
    read_solar_system(fp, ss);

    fclose(fp);
    
} 
