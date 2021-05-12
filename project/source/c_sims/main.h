// this file will contain the function defns etc, all basically so the file can be organised with a make file
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#include <omp.h>

// check this is the correct size!
//will want to read all this in soon!
#define ITERS 500000
#define MAX_BODIES 10
#define G 2.96*pow(10, -4)
#define DT 0.01
#define TIME_FILE "source/results/time.txt"
#define OUTPUT_FILE "source/results/data.txt" //not certain this is needed
//may need to change
#define TIMES_RECORDED 8

typedef struct {
    long double x;
    long double y;
    long double vx;
    long double vy;
    long double ax;
    long double ay;
    long double radius; //not sure this is needed yet!
    long double mass;
} body_t;


// stores the array of the times
// this works as intended but time only goes to seconds!
//need to use something else
typedef struct {
    struct timeval start;
    struct timeval stop;
    float times[TIMES_RECORDED];
    int recorded;
} timer_t;

// not sure if this is good, may be better to just have an array of the bodies??
// as there will always be MAX_BODIES in there
//this struct should defs be used, its more robust for variable planets
// and it can store the iters_complete so that each body doesn;t have to store it!
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
