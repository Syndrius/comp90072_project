/* Written by Matthew Thomas 831343, May 2021 for COMP90072 at unimelb
 *
 * Header file that contains the definitions for functions, structs and constants
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
#define TIME_FILE "source/data/time.txt"
#define OUTPUT_FILE "source/data/data.txt" 
#define TIMES_RECORDED 8


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

// function declerations
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
void free_pos_history(long double **pos_history, int iters);
void free_ss(solar_system_t *ss);
