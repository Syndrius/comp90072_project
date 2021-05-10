// this file will contain the function defns etc, all basically so the file can be organised with a make file
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>

// check this is the correct size!
//will want to read all this in soon!
#define ITERS 500000
#define MAX_BODIES 10
#define G 2.96*pow(10, -4)
#define DT 0.01
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
    int iters_complete;
    body_t bodies[MAX_BODIES];
    int num_bodies;
    int max_iters;
} solar_system_t;


void read_solar_system(FILE *fp, solar_system_t *ss);
void simulation(solar_system_t *ss, long double** pos_historyi, timer_t *timer);
void update_bodies(solar_system_t *ss, long double *pos_history);
float timedifference_msec(struct timeval t0, struct timeval t1);
