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

// change this to return array of doubles
void base_simulation(solar_system_t *ss, long double **pos_history, timer_t *timer) {
    int i, j, k;
    long double y_diff, x_diff;
    long double angle, a1, a2, force;
    time_t seconds;
    //may be better to make a vector type [x, y]
    //but this ensures comparison to python
    long double * ax = malloc(ss->num_bodies*sizeof(long double));
    long double * ay = malloc(ss->num_bodies*sizeof(long double));

    printf("made it to sim\n");   


    for (i=0;i<ss->max_iters;i++) {
    //for (i=0;i<5;i++) {
        // this is gross
        if ((i == ss->max_iters/5 * 1) || (i == ss->max_iters/5 * 2) || (i == ss->max_iters/5 * 3) || (i == ss->max_iters/5 * 4)) {
            gettimeofday(&timer->stop, NULL);
            timer->times[timer->recorded] = timedifference_msec(timer->start, timer->stop);
            timer->recorded += 1;
        }
            
        //resets the acceleration to zero
        ax = memset(ax, 0, ss->num_bodies*sizeof(long double));
        ay = memset(ay, 0, ss->num_bodies*sizeof(long double));
        /*
        if (i==1) { 
            for (j=0;j<10;j++) {
                printf("%Lf\n", ax[j]);
            }   
        }
        */
        for (j=0;j<ss->num_bodies;j++) {

            for (k=j+1; k<ss->num_bodies;k++) {
                
                y_diff = ss->y[k] - ss->y[j];

                x_diff = ss->x[k] - ss->x[j];


                //need to make sure this does the same thing as python!
                angle = atan2(y_diff, x_diff);


                // may be a better option for squaring!
                force = G*ss->mass[k]*ss->mass[j]/(x_diff*x_diff + y_diff*y_diff);

                a1 = force/ss->mass[j];
                a2 = force/ss->mass[k];


                // this is where it gets spicy, need to make sure this update carries
                // over the the main ss object!
                ax[j] += a1*cos(angle);
                ay[j] += a1*sin(angle);

                ax[k] += a2*cos(angle + M_PI);
                ay[k] += a2*sin(angle + M_PI);
            }
        }
        //printf("%Lf\n", ax[1]);
        ss->iters_complete += 1;
        //updates each bodies position and velocity
        
        update_bodies(ss, pos_history[i], ax, ay);
    }

}

// change this to return array of doubles
void multi_simulation(solar_system_t *ss, long double **pos_history, timer_t *timer) {
    int i, j, k;
    long double y_diff, x_diff;
    long double angle, a1, a2, force, dist, dist_cubed;
    time_t seconds;
    //may be better to make a vector type [x, y]
    //but this ensures comparison to python
    //long double * ax = malloc(ss->num_bodies*sizeof(long double));
    //long double * ay = malloc(ss->num_bodies*sizeof(long double));


    //try define a's in asic way!
    long double ax[ss->num_bodies];
    long double ay[ss->num_bodies];
    long double x[ss->num_bodies];
    long double y[ss->num_bodies];
    long double mass[ss->num_bodies];
    //to store acceleration before it is split up
    //may want to define a type for this!
    long double a[2];

    printf("made it to sim\n");   


    for (i=0;i<ss->max_iters;i++) {
    //for (i=0;i<5;i++) {
        // this is gross
        if ((i == ss->max_iters/5 * 1) || (i == ss->max_iters/5 * 2) || (i == ss->max_iters/5 * 3) || (i == ss->max_iters/5 * 4)) {
            gettimeofday(&timer->stop, NULL);
            timer->times[timer->recorded] = timedifference_msec(timer->start, timer->stop);
            timer->recorded += 1;
        }
            
        //resets the acceleration to zero
        memset(ax, 0, ss->num_bodies*sizeof(long double));
        memset(ay, 0, ss->num_bodies*sizeof(long double));
        //printf("set mem to 0\n");
        for (int q=0; q<ss->num_bodies;q++) {
            ax[q] = 0;
            ay[q] = 0;
        }
        /*
        if (i==1) { 
            for (j=0;j<10;j++) {
                printf("%Lf\n", ax[j]);
            }   
        }
        
        */
        //memcpy(x, ss->x, ss->num_bodies*sizeof(long double));
        //memcpy(y, ss->y, ss->num_bodies*sizeof(long double));
        //memcpy(mass, ss->mass, ss->num_bodies*sizeof(long double));
        //tells openmp to parralise 2 nested for loops
        //ordered might change the way it does it
        #pragma omp parallel for private(a, x, y, mass, dist_cubed, y_diff, x_diff, dist, force, a1) reduction(+:ax) reduction(+:ay)
        for (j=0;j<ss->num_bodies;j++) {
            //ax[j] =0;
            //ay[j] = 0;
            //a = malloc(2*sizeof(long double));
            multi_compute_a(ss, j, a);
            ax[j] = a[0];
            ay[j] = a[1];
        }
        //printf("%Lf\n", ax[1]);
        ss->iters_complete += 1;
        //updates each bodies position and velocity
        
        update_bodies(ss, pos_history[i], ax, ay);
    }

}

// This works! I guess it stops each thread reading same bit of memory?
void multi_compute_a(solar_system_t *ss, int index, long double *a) {
    long double y_diff, x_diff, angle, force;
    //long double a[2];
    a[0] = 0;
    a[1] = 0;

    for (int k=0; k<ss->num_bodies;k++) {
        //dont count self 
        if (index==k){
            continue;
        }
        
        y_diff = ss->y[k] - ss->y[index];
        
        x_diff = ss->x[k] - ss->x[index];
        
        //y_diff = y[k] - y[j];
        //x_diff = x[k] - x[j];



        //need to make sure this does the same thing as python!
        angle = atan2(y_diff, x_diff);

        //dist = sqrt(x_diff*x_diff + y_diff*y_diff);
        //dist_cubed = dist*dist*dist;

        // may be a better option for squaring!
        //should change this!
        force = G*ss->mass[k]/(x_diff*x_diff + y_diff*y_diff+0.005);
        //force = 1;

        //a1 = force/ss->mass[j];
        //a2 = force/ss->mass[k];


        // this is where it gets spicy, need to make sure this update carries
        // over the the main ss object!
        a[0] += force*cos(angle);
        a[1] += force*sin(angle);
        
        //ax[j] += G*ss->mass[k]/dist_cubed * x_diff;
        //#pragma omp reduction(+:sum)
        //ay[j] += G*ss->mass[k]/dist_cubed * y_diff;
        
        //ax[k] += a2*cos(angle + M_PI);
        //ay[k] += a2*sin(angle + M_PI);
    }
}

void update_bodies(solar_system_t *ss, long double *pos_history, long double *ax, long double *ay) {
    int i;
    //printf("%Lf\n", ay[1]);

    for (i=0;i<ss->num_bodies;i++) {
        ss->x[i] += ss->vx[i]*DT;
        ss->y[i] += ss->vy[i]*DT;
        ss->vx[i] += ax[i]*DT;
        ss->vy[i] += ay[i]*DT;
        //printf("%Lf\n", ss->x[i]);
        //printf("%Lf\n", ss->vx[i]);
        pos_history[2*i] = ss->x[i];
        pos_history[2*i+1] = ss->y[i];
        
    /*
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
        */
    }
}


// this is defined twice which is no good
float timedifference_msec(struct timeval t0, struct timeval t1)
{
    return (t1.tv_sec - t0.tv_sec) * 1000.0f + (t1.tv_usec - t0.tv_usec) / 1000.0f;
}
