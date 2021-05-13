/* 
 * Header file that contains the definitions for functions, structs and constants
 *
 *
 *
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <omp.h>

#define G 2.96*pow(10, -4)
#define DT 0.01
#define TIME_FILE "source/results/time.txt"
#define OUTPUT_FILE "source/results/data.txt" 
// may need to change
#define TIMES_RECORDED 8

// stores the array of the times
// this works as intended but time only goes to seconds!
//need to use something else
// Struct for keeping track of the time taken for sims to run
typedef struct {
    struct timeval start;
    struct timeval stop;
    float times[TIMES_RECORDED];
    int recorded;
} timer_t;


// Main struct that stores the position and velocities of each body
typedef struct {
    long double *x;
    long double *y;
    long double *vx;
    long double *vy;
    long double *mass;
    int max_bodies;
    int iters_complete;
    int num_bodies;
    int max_iters;
} solar_system_t;


void read_solar_system(FILE *fp, solar_system_t *ss);
void base_simulation(solar_system_t *ss, long double** pos_history, timer_t *timer);
void multi_simulation(solar_system_t *ss, long double** pos_history, timer_t *timer);
void update_bodies(solar_system_t *ss, long double *pos_history, long double *ax, long double *ay);
float timedifference_msec(struct timeval t0, struct timeval t1);
void multi_compute_a(solar_system_t *ss, int index, long double *a);
void init_ss(char *coord_file, solar_system_t *ss, int iters, int num_bodies);
void init_pos_history(long double **pos_history, int iters, int size);
void run_multi_sim(solar_system_t *ss);
void run_base_sim(solar_system_t *ss);
void write_time(char *time_file, timer_t *timer, char* label);
void write_pos(char *output_file, long double **pos_history, int iters, int size);
