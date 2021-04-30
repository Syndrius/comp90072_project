//stores the simulation functions 

#include "c_main.h"

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
        //ss->bodies[ss->num_bodies].x_positions = malloc(ITERS*sizeof(long double));
        //ss->bodies[ss->num_bodies].y_positions = malloc(ITERS*sizeof(long double));
        //ss->bodies[ss->num_bodies].x_positions[0] = ss->bodies[ss->num_bodies].x;
        //ss->bodies[ss->num_bodies].y_positions[0] = ss->bodies[ss->num_bodies].y;
        ss->num_bodies += 1;
    }
}

// change this to return array of doubles
void simulation(solar_system_t *ss, long double **pos_history, timer_t *timer) {
    int i, j, k;
    long double y_diff, x_diff;
    long double angle, a1, a2, force;
    time_t seconds;
    body_t *body1, *body2;
    printf("made it to sim\n");   


    for (i=0;i<ITERS;i++) {

        if ((i == ITERS/5 * 1) || (i == ITERS/5 * 2) || (i == ITERS/5 * 3) || (i == ITERS/5 * 4)) {
            gettimeofday(&timer->stop);
            timer->times[timer->recorded] = timedifference_msec(timer->start, timer->stop);
            timer->recorded += 1;
        }
            
       
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
        
        update_bodies(ss, pos_history[i]);
    }

}


void update_bodies(solar_system_t *ss, long double *pos_history) {
    int i;

    for (i=0;i<ss->num_bodies;i++) {
        ss->bodies[i].x += ss->bodies[i].vx*DT;
        ss->bodies[i].y += ss->bodies[i].vy*DT;
    

        ss->bodies[i].vx += ss->bodies[i].ax*DT;
        ss->bodies[i].vy += ss->bodies[i].ay*DT;
        

        //ss->bodies[i].x_positions[ss->iters_complete] = ss->bodies[i].x;
        //ss->bodies[i].y_positions[ss->iters_complete] = ss->bodies[i].y;

        ss->bodies[i].ax = 0;
        ss->bodies[i].ay = 0;
       // printf("updated most\n");
        pos_history[2*i] = ss->bodies[i].x;
        pos_history[2*i+1] = ss->bodies[i].y;
        //printf("added to array\n");
    }
}


// this is defined twice which is no good
float timedifference_msec(struct timeval t0, struct timeval t1)
{
    return (t1.tv_sec - t0.tv_sec) * 1000.0f + (t1.tv_usec - t0.tv_usec) / 1000.0f;
}
