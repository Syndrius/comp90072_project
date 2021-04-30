// this file will contain the function defns etc, all basically so the file can be organised with a make file
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

// check this is the correct size!
//will want to read all this in soon!
#define ITERS 500000
#define MAX_BODIES 10
#define G 2.96*pow(10, -4)
#define DT 0.01

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

// not sure if this is good, may be better to just have an array of the bodies??
// as there will always be MAX_BODIES in there
//this struct should defs be used, its more robust for variable planets
// and it can store the iters_complete so that each body doesn;t have to store it!
typedef struct {
    int iters_complete;
    body_t bodies[MAX_BODIES];
    int num_bodies;
} solar_system_t;


void read_solar_system(FILE *fp, solar_system_t *ss);
void simulation(solar_system_t *ss, long double** pos_history);
void update_bodies(solar_system_t *ss, long double *pos_history);

