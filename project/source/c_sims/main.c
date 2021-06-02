/* Written by Matthew Thomas 831343, May 2021 for COMP90072 at unimelb
 *
 * main c file, creates the solar system object then reads in 
 * command line arguments then calls the simulations
 *
 */

#include "main.h"


int main(int argc, char *argv[]) {

    //Creates the main solar_system struct
    solar_system_t ss;
    
    
    //ensures command line args are correct
    if (argc < 2) {
        printf("Error with command line arguments.\n");
        return 0;
    }

    //Reads the command line arguments
    char *coord_file = argv[1];
    int iters = atoi(argv[2]);
    int num_bodies = atoi(argv[3]);


    //Initialise the ss, and reads the initial data
    init_ss(coord_file, &ss, iters, num_bodies);

    //Runs both simulations 
    if (argc == 6) {
        printf("Running basic simulation...\n");
        run_base_sim(&ss);
        printf("Running multiprocessing simulation...\n");
        run_multi_sim(&ss);
    }
    //Runs the basic simulation
    else if (!strcmp(argv[4], "b")) {
        printf("Running basic simulation...\n");
        run_base_sim(&ss);
    }
    //Runs the multiprocessing simulation
    else {
        printf("Running multiprocessing simulation...\n");
        run_multi_sim(&ss);
    }
    free_ss(&ss);

    return 0;

}
 
