/* Written by Matthew Thomas 831343, May 2021 for COMP90072 at unimelb
 * 
 * Contains the simulation functions
 *
 */

#include "main.h"


/* Basic simulation */
void base_simulation(solar_system_t *ss, long double **pos_history, timer_t *timer) {
    int i, j, k;
    long double y_diff, x_diff;
    long double angle, a1, a2, force;
    long double * ax = malloc(ss->num_bodies*sizeof(long double));
    long double * ay = malloc(ss->num_bodies*sizeof(long double));


    for (i=0;i<ss->max_iters;i++) {

        // measures the time at set intervals
        if ((i == ss->max_iters/5 * 1) || (i == ss->max_iters/5 * 2) || (i == ss->max_iters/5 * 3) || (i == ss->max_iters/5 * 4)) {
            gettimeofday(&timer->stop, NULL);
            timer->times[timer->recorded] = timedifference_msec(timer->start, timer->stop);
            timer->recorded += 1;
        }
            
        //resets the acceleration to zero
        ax = memset(ax, 0, ss->num_bodies*sizeof(long double));
        ay = memset(ay, 0, ss->num_bodies*sizeof(long double));

        for (j=0;j<ss->num_bodies;j++) {

            for (k=j+1; k<ss->num_bodies;k++) {
                
                y_diff = ss->y[k] - ss->y[j];

                x_diff = ss->x[k] - ss->x[j];


                // Computes the angle between the bodies
                angle = atan2(y_diff, x_diff);


                // Computes the force
                force = G*ss->mass[k]*ss->mass[j]/(x_diff*x_diff + y_diff*y_diff);

                a1 = force/ss->mass[j];
                a2 = force/ss->mass[k];


                ax[j] += a1*cos(angle);
                ay[j] += a1*sin(angle);

                ax[k] += a2*cos(angle + M_PI);
                ay[k] += a2*sin(angle + M_PI);
            }
        }
        ss->iters_complete += 1;

        //updates each bodies position and velocity
        update_bodies(ss, pos_history[i], ax, ay);
    }
    free(ax);
    free(ay);

}

/* Simulation with multiprocessing */
void multi_simulation(solar_system_t *ss, long double **pos_history, timer_t *timer) {
    int i, j;
    long double ax[ss->num_bodies];
    long double ay[ss->num_bodies];
    long double a[2];



    for (i=0;i<ss->max_iters;i++) {

        // this is gross
        if ((i == ss->max_iters/5 * 1) || (i == ss->max_iters/5 * 2) || (i == ss->max_iters/5 * 3) || (i == ss->max_iters/5 * 4)) {
            gettimeofday(&timer->stop, NULL);
            timer->times[timer->recorded] = timedifference_msec(timer->start, timer->stop);
            timer->recorded += 1;
        }
            
        //resets the acceleration to zero
        memset(ax, 0, ss->num_bodies*sizeof(long double));
        memset(ay, 0, ss->num_bodies*sizeof(long double));

        //tells openmp to parralise this for loop
        #pragma omp parallel for private(a) reduction(+:ax) reduction(+:ay)
        for (j=0;j<ss->num_bodies;j++) {
            multi_compute_a(ss, j, a);
            ax[j] = a[0];
            ay[j] = a[1];
        }
        ss->iters_complete += 1;

        //updates each bodies position and velocity
        update_bodies(ss, pos_history[i], ax, ay);
    }

}

/* Computes the acceleration of each body */
void multi_compute_a(solar_system_t *ss, int index, long double *a) {

    long double y_diff, x_diff, angle, force;
    a[0] = 0;
    a[1] = 0;

    for (int k=0; k<ss->num_bodies;k++) {

        //dont count self 
        if (index==k){
            continue;
        }
        
        y_diff = ss->y[k] - ss->y[index];
        
        x_diff = ss->x[k] - ss->x[index];
        
        
        // computes the angle between bodies
        angle = atan2(y_diff, x_diff);


        force = G*ss->mass[k]/(x_diff*x_diff + y_diff*y_diff+0.005);
        
        a[0] += force*cos(angle);
        a[1] += force*sin(angle);
        
    }
}

/* Updates the positions and velocities of the bodies */
void update_bodies(solar_system_t *ss, long double *pos_history, long double *ax, long double *ay) {
    int i;

    for (i=0;i<ss->num_bodies;i++) {
        ss->x[i] += ss->vx[i]*DT;
        ss->y[i] += ss->vy[i]*DT;
        ss->vx[i] += ax[i]*DT;
        ss->vy[i] += ay[i]*DT;
        pos_history[2*i] = ss->x[i];
        pos_history[2*i+1] = ss->y[i];
        
    }
}


