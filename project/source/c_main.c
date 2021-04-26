// currently writes to same location as python script, can be changed later!
// dont think it matters though, plotting the trajectories is not that important
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
    long double *x_positions;
    long double *y_positions;
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
void simulation(solar_system_t *ss);
void update_bodies(solar_system_t *ss);

int main(int argc, char *argv[]) {
    //file scanning requires a buffer to scan into!
    //this is the file pointer
    FILE *fp;
    //creates the main solar_system struct
    solar_system_t ss;

    ss.num_bodies = 0;
    ss.iters_complete = 0;


    fp = fopen("source/planet_coords.txt", "r");
    
    //probably should have a file error guard here!
    
    //reads the initial coordinates into ss 
    read_solar_system(fp, &ss);

    fclose(fp);
   
    //runs the simulation
    simulation(&ss);


    int j, k;

    //for (j=0; j<ss.iters_complete; j++) {
    //    printf("%.15Lf %.15Lf \n", ss.bodies[0].x_positions[j], ss.bodies[0].y_positions[j]);
    //}
    char output_file[] = "source/results/data_body_0.txt";
    char c;

    //create a func for this! 
    for (j=0;j<ss.num_bodies; j++) {
        // need a guard for this!!!
        //horrofic solution, only works for integers < 10 which is lucky!!!
        // really should change this, -> maybe bash generating the files is
        // the best bet??? and just use argv etc
        c = j + '0';
        output_file[25] = c;
        fp = fopen(output_file, "w");
        //need guards!
        for (k=0;k<ss.iters_complete;k++) {
            fprintf(fp, "%Lf %Lf\n", ss.bodies[j].x_positions[k], ss.bodies[j].y_positions[k]);
        }

        fclose(fp);
    }
    
    //should be some kind of return thing here lol

}

//this works! may not be passing the things around properly
//ie pointers vs not pointers!
void read_solar_system(FILE *fp, solar_system_t *ss) {
    //nothing stopiing bodies read being more than MAX_BODIES
    //maybe add some kind of guard?
    //second condition is very important
    // who wouldve thunked it!
    while (!feof(fp) && (ss->num_bodies < MAX_BODIES)) {
        fscanf(fp, "%Lf %Lf %Lf %Lf %Lf %Lf",
            &ss->bodies[ss->num_bodies].x, 
            &ss->bodies[ss->num_bodies].y, 
            &ss->bodies[ss->num_bodies].vx, 
            &ss->bodies[ss->num_bodies].vy, 
            &ss->bodies[ss->num_bodies].radius, 
            &ss->bodies[ss->num_bodies].mass);
        //why no & for this?
        //printf("%Lf\n", ss->bodies[ss->num_bodies].ax);
        ss->bodies[ss->num_bodies].ax = 0;
        ss->bodies[ss->num_bodies].ay = 0;
        //need to use malloc for this
        // allocating memory in struct doesn't have enough space
        // malloc puts the memory somewhere else
        ss->bodies[ss->num_bodies].x_positions = malloc(ITERS*sizeof(long double));
        ss->bodies[ss->num_bodies].y_positions = malloc(ITERS*sizeof(long double));
        ss->bodies[ss->num_bodies].x_positions[0] = ss->bodies[ss->num_bodies].x;
        ss->bodies[ss->num_bodies].y_positions[0] = ss->bodies[ss->num_bodies].y;
        ss->num_bodies += 1;
    }
}


void simulation(solar_system_t *ss) {
    int i, j, k;
    long double y_diff, x_diff;
    long double angle, a1, a2, force;
    body_t *body1, *body2;

    for (i=0;i<ITERS;i++) {
       
       for (j=0;j<ss->num_bodies;j++) {
            body1 = &ss->bodies[j];

            for (k=j+1; k<ss->num_bodies;k++) {
                body2 = &ss->bodies[k];
                
                y_diff = body2->y - body1->y;

                x_diff = body2->x - body1->x;

                //need to make sure this does the same thing as python!
                angle = atan2(y_diff, x_diff);


                // may be a better option for squaring!
                force = G*body1->mass*body2->mass/(x_diff*x_diff + y_diff*y_diff);

                a1 = force/body1->mass;
                a2 = force/body2->mass;


                // this is where it gets spicy, need to make sure this update carries
                // over the the main ss object!
                body1->ax += a1*cos(angle);
                body1->ay += a1*sin(angle);

                body2->ax += a2*cos(angle + M_PI);
                body2->ay += a2*sin(angle + M_PI);
            }
        }
        ss->iters_complete += 1;
        //updates each bodies position and velocity
        update_bodies(ss);
    }

}


void update_bodies(solar_system_t *ss) {
    int i;

    for (i=0;i<ss->num_bodies;i++) {
        ss->bodies[i].x += ss->bodies[i].vx*DT;
        ss->bodies[i].y += ss->bodies[i].vy*DT;
    

        ss->bodies[i].vx += ss->bodies[i].ax*DT;
        ss->bodies[i].vy += ss->bodies[i].ay*DT;
        

        ss->bodies[i].x_positions[ss->iters_complete] = ss->bodies[i].x;
        ss->bodies[i].y_positions[ss->iters_complete] = ss->bodies[i].y;

        ss->bodies[i].ax = 0;
        ss->bodies[i].ay = 0;
    }
}
