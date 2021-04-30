// currently writes to same location as python script, can be changed later!
// dont think it matters though, plotting the trajectories is not that important

#include "c_main.h"


int main(int argc, char *argv[]) {
    //file scanning requires a buffer to scan into!
    //this is the file pointer
    FILE *fp;
    //defining this twice, may be better to pass the pointer in
    long double** pos_history;
    //creates the main solar_system struct
    solar_system_t ss;

    ss.num_bodies = 0;
    ss.iters_complete = 0;


    fp = fopen("source/planet_coords.txt", "r");
    
    //probably should have a file error guard here!
    
    //reads the initial coordinates into ss 
    read_solar_system(fp, &ss);

    fclose(fp);

    // 2 for x, y
    pos_history = malloc(ITERS * sizeof(*pos_history));
    int i, j;
    for (i=0;i<ITERS;i++) {
        // creates the memory for each inner array, 2 is for 2 coords for each body
        // could be worth defining a vec type that stores two long doubles
        pos_history[i] = malloc(2*ss.num_bodies*sizeof(**pos_history));
    }
    //printf("got to here\n");   
    //runs the simulation
    simulation(&ss, pos_history);
    printf("got to here\n");   
    printf("%.15Lf\n", pos_history[100][0]);
    char output_file[] = "source/results/data.txt";

    for (i=0;i<2*ss.num_bodies;i++) {
        printf("%.15Lf\n", pos_history[0][i]);
    }
    //This ensures the file is empty before appending to it
    fp = fopen(output_file, "w");
    fclose(fp);
    fp = fopen(output_file, "a");

    //fwrite(pos_history[2], sizeof(**pos_history), 2*ss.num_bodies, fp);
    //this is terrible but it works
    for (i=0;i<ITERS;i++) {
        for (j=0;j<2*ss.num_bodies;j++) {
            if (j==2*ss.num_bodies-1) {
                fprintf(fp, "%.15Lf", pos_history[i][j]);
            }
            else {
                fprintf(fp, "%.15Lf ", pos_history[i][j]);
            }
        }
        fprintf(fp, "\n");
        // could be worth defining 2*ss.numbodies    
        //fwrite(pos_history[i], sizeof(**pos_history), 2*ss.num_bodies, fp);
    }
    
    fclose(fp);

    /*
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
    */
    
    //should be some kind of return thing here lol

}

