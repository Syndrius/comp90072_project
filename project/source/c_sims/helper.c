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


void write_time(char *time_file, timer_t *timer, char* label) {
    FILE *fp;
    //label tells which sim 
    fp = fopen(time_file, "a");
    for (int i=0;i<timer->recorded;i++) {
        fprintf(fp, "%f ", timer->times[i]/1000);
    }
    fprintf(fp, "%s\n", label);
    fclose(fp);
}



void run_base_sim(solar_system_t *ss) {
    timer_t timer;
    long double **pos_history;

    printf("%d\n", ss->max_iters);
    pos_history = malloc(ss->max_iters * sizeof(*pos_history));
    init_pos_history(pos_history, ss->max_iters, ss->max_bodies);
    

    //initialise the timer
    gettimeofday(&timer.start, NULL);
    timer.recorded = 0;
    // this value may need to change
    // sets the intial time
    timer.times[timer.recorded] = 0;
    timer.recorded += 1;

    base_simulation(ss, pos_history, &timer);
    //gets the time after the sim is complete
    gettimeofday(&timer.stop, NULL);
    timer.times[timer.recorded] = timedifference_msec(timer.start, timer.stop);
    timer.recorded += 1;

    //need to define output file, and time file
    write_pos(OUTPUT_FILE, pos_history, ss->max_iters, ss->max_bodies);
    
    // records time after file write
    gettimeofday(&timer.stop, NULL);
    timer.times[timer.recorded] = timedifference_msec(timer.start, timer.stop);
    timer.recorded += 1;

    write_time(TIME_FILE, &timer, "cb");

}

void run_multi_sim(solar_system_t *ss) {
    timer_t timer;
    long double **pos_history;

    pos_history = malloc(ss->max_iters * sizeof(*pos_history));
    init_pos_history(pos_history, ss->max_iters, ss->max_bodies);

    //initialise the timer
    gettimeofday(&timer.start, NULL);
    timer.recorded = 0;
    // this value may need to change
    // sets the intial time
    timer.times[timer.recorded] = 0;
    timer.recorded += 1;

    multi_simulation(ss, pos_history, &timer);
    //gets the time after the sim is complete
    gettimeofday(&timer.stop, NULL);
    timer.times[timer.recorded] = timedifference_msec(timer.start, timer.stop);
    timer.recorded += 1;

    //need to define output file, and time file

    write_pos(OUTPUT_FILE, pos_history, ss->max_iters, ss->max_bodies);
    
    // records time after file write
    gettimeofday(&timer.stop, NULL);
    timer.times[timer.recorded] = timedifference_msec(timer.start, timer.stop);
    timer.recorded += 1;

    write_time(TIME_FILE, &timer, "cm");


}

//need to check form of this!
// allocates the memory of the 2d array
void init_pos_history(long double **pos_history, int iters, int size) {
    //pos_history = malloc(iters * sizeof(*pos_history));
    for (int i=0;i<iters;i++) {
        // creates the memory for each inner array, 2 is for 2 coords fo
        // could be worth defining a vec type that stores two long doubl
        pos_history[i] = malloc(2*size*sizeof(**pos_history));
    }
}

void read_solar_system(FILE *fp, solar_system_t *ss) {
    //nothing stopiing bodies read being more than MAX_BODIES
    //maybe add some kind of guard?
    //second condition is very important
    // who wouldve thunked it!
    while (!feof(fp) && (ss->num_bodies < MAX_BODIES)) {
        fscanf(fp, "%Lf %Lf %Lf %Lf %Lf",
            &ss->x[ss->num_bodies],
            &ss->y[ss->num_bodies],
            &ss->vx[ss->num_bodies],
            &ss->vy[ss->num_bodies],
            &ss->mass[ss->num_bodies]);

            /*
            &ss->bodies[ss->num_bodies].x, 
            &ss->bodies[ss->num_bodies].y, 
            &ss->bodies[ss->num_bodies].vx, 
            &ss->bodies[ss->num_bodies].vy, 
            &ss->bodies[ss->num_bodies].radius, 
            &ss->bodies[ss->num_bodies].mass);
            */
        //why no & for this?
        //printf("%Lf\n", ss->bodies[ss->num_bodies].ax);
        //ss->bodies[ss->num_bodies].ax = 0;
        //ss->bodies[ss->num_bodies].ay = 0;
        //need to use malloc for this
        // allocating memory in struct doesn't have enough space
        // malloc puts the memory somewhere else
        //ss->bodies[ss->num_bodies].x_positions = malloc(ss->max_iters*sizeof(long double));
        //ss->bodies[ss->num_bodies].y_positions = malloc(ss->max_iters*sizeof(long double));
        //ss->bodies[ss->num_bodies].x_positions[0] = ss->bodies[ss->num_bodies].x;
        //ss->bodies[ss->num_bodies].y_positions[0] = ss->bodies[ss->num_bodies].y;
        ss->num_bodies += 1;
    }
}

// this is defined twice which is no good
float timedifference_msec(struct timeval t0, struct timeval t1)
{
    return (t1.tv_sec - t0.tv_sec) * 1000.0f + (t1.tv_usec - t0.tv_usec) / 1000.0f;
}

void init_ss(char *coord_file, solar_system_t *ss, int iters, int num_bodies) {
    FILE *fp;
    //probs want a function that initialises all these structs
    ss->num_bodies = 0;
    ss->iters_complete = 0;
    ss->max_iters = iters;
    ss->max_bodies = num_bodies;

    // creates the arrays for storing the positions etc
    //needs to be done in a function!
    ss->x = malloc(ss->max_bodies*sizeof(long double));
    ss->y = malloc(ss->max_bodies*sizeof(long double));
    ss->vx = malloc(ss->max_bodies*sizeof(long double));
    ss->vy = malloc(ss->max_bodies*sizeof(long double));
    ss->mass = malloc(ss->max_bodies*sizeof(long double));

    fp = fopen(coord_file, "r");
    
    //probably should have a file error guard here!
    
    //reads the initial coordinates into ss 
    read_solar_system(fp, ss);

    fclose(fp);
    
} 
