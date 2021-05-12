// currently writes to same location as python script, can be changed later!
// dont think it matters though, plotting the trajectories is not that important
// need to start adding in free() and guards for files etc

#include "main.h"


int main(int argc, char *argv[]) {
    //file scanning requires a buffer to scan into!
    //this is the file pointer
    FILE *fp;
    //defining this twice, may be better to pass the pointer in
    long double** pos_history;
    //creates the main solar_system struct
    solar_system_t ss;// = malloc(sizeof(solar_system_t));


    //probabaly want a guard for this!
    char *coord_file = argv[1];
    int iters = atoi(argv[2]);
    int num_bodies = atoi(argv[3]);
    printf("%d\n", argc); 
    printf("%s\n", argv[4]);
    pos_history = malloc(iters*sizeof(*pos_history));
    //initialise the ss obj, and reads the initial data
    //may want some kind of timer for this!
    init_ss(coord_file, &ss, iters, num_bodies);

    //need to initialise and read file before doing this!
    //both_sims need to be run
    if (argc == 6) {
        printf("Both sims\n");
        run_base_sim(&ss);
        run_multi_sim(&ss);
    }
    else if (!strcmp(argv[4], "b")) {
        printf("Base sim\n");
        run_base_sim(&ss);
    }
    else {
        printf("Multi sim\n");
        run_multi_sim(&ss);
    }
    printf("%d\n", iters);
    printf("%d\n", num_bodies);


    timer_t timer;
    //should be getting the initial time
    gettimeofday(&timer.start, NULL);
    timer.recorded = 0;
    // this value may need to change
    // sets the intial time
    timer.times[timer.recorded] = 0;
    timer.recorded += 1;
 

    //bug testing
    /* 
    //int k;
    printf("%d\n", ss.max_bodies);
    for (k=0;k<ss.max_bodies;k++) {
        printf("%Lf, %Lf, %Lf, %Lf, %Lf\n", ss.x[k], ss.y[k], ss.vx[k], ss.vy[k], ss.mass[k]);
    }
    */

    //this wont work to well for multiple c funcs, 
    // will need to create multiple timer objs
    gettimeofday(&timer.stop, NULL);
    timer.times[timer.recorded] = timedifference_msec(timer.start, timer.stop);
    timer.recorded += 1;
    

    // 2 for x, y
    /*
    pos_history = malloc(ss.max_iters * sizeof(*pos_history));
    int i, j;
    for (i=0;i<ss.max_iters;i++) {
        // creates the memory for each inner array, 2 is for 2 coords for each body
        // could be worth defining a vec type that stores two long doubles
        pos_history[i] = malloc(2*ss.num_bodies*sizeof(**pos_history));
    }
    */
    //printf("got to here\n");   
    //runs the simulation
    //multi_simulation(&ss, pos_history, &timer);
    
    //gets the time after the sim is complete
    gettimeofday(&timer.stop, NULL);
    timer.times[timer.recorded] = timedifference_msec(timer.start, timer.stop);
    timer.recorded += 1;
 
    //printf("got to here\n");   
    //printf("%.15Lf\n", pos_history[100][0]);
    //probs define this is main.h??
    char output_file[] = "source/results/data.txt";
    /*
    for (i=0;i<2*ss.num_bodies;i++) {
        printf("%.15Lf\n", pos_history[0][i]);
    }*/
    /*
    //This ensures the file is empty before appending to it
    fp = fopen(output_file, "w");
    fclose(fp);
    fp = fopen(output_file, "a");

    //fwrite(pos_history[2], sizeof(**pos_history), 2*ss.num_bodies, fp);
    //this is terrible but it works
    for (i=0;i<ss.max_iters;i++) {
        for (j=0;j<2*ss.num_bodies;j++) {
            if (j==2*ss.num_bodies-1) {
                fprintf(fp, "%.15Lf", pos_history[i][j]);
            }
            //this is to deal with the need for whitespace
            // but don't want whitespace at the end!
            else {
                fprintf(fp, "%.15Lf ", pos_history[i][j]);
            }
        }
        fprintf(fp, "\n");
        // could be worth defining 2*ss.numbodies    
        //fwrite(pos_history[i], sizeof(**pos_history), 2*ss.num_bodies, fp);
    }
    
    fclose(fp);
    */
    //this works, gettimeofday may be outdated tho!
    gettimeofday(&timer.stop, NULL);
    timer.times[timer.recorded] = timedifference_msec(timer.start, timer.stop);
    timer.recorded += 1;

    //may be wrong name!
    char time_file[] = "source/results/time.txt";

    /*
    // bash deletes file contents so always append
    //really need file protection for all of this
    fp = fopen(time_file, "a");


    for (i=0;i<timer.recorded;i++) {
        fprintf(fp, "%f ", timer.times[i]/1000);
    }
    fprintf(fp, "c\n");
    fclose(fp);
    */


    
    //should be some kind of return thing here lol

}
 
