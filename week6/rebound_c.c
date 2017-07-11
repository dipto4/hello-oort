#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
#include <omp.h>
#include "rebound.h"
#include "tools.h"
#include "output.h"

void run_sim() {
	struct reb_simulation* const r = reb_create_simulation_from_binary("initial.in");
	r->integrator = REB_INTEGRATOR_IAS15;
	r->gravity = REB_GRAVITY_BASIC;
	r->boundary = REB_BOUNDARY_NONE;
	r->softening = 0.02;
    r->opening_angle2 = 1.5;
    r->collision_resolve_keep_sorted = 1;
    r->testparticle_type = 1;

    reb_output_binary(r , "data/data0.in");
    char filename[50];
	float t = 0.0;
	float t_final = 30e6;
    int i = 0;
	
    reb_integrate(r,1000);
    reb_output_binary(r,"data/data1.in");   
    
    //while (t < t_final) {
	//	t+=1000;
	//	reb_integrate(r,t);
    //   printf("%i \n",i++);
    //    sprintf(filename, "data/data%d.in",i);
    //    reb_output_binary(r,filename);
	//}

	reb_free_simulation(r);

}


int main(int argc, char * argv[]) {
	int np = omp_get_num_procs();
     // Set the number of OpenMP threads to be the number of processors
     omp_set_num_threads(np);


     // First, run it with the OpenMP turned on.
     struct timeval tim;
     gettimeofday(&tim, NULL);
     double timing1 = tim.tv_sec+(tim.tv_usec/1000000.0);
     run_sim();

     // Reduce the number of threads to 1 and run again.
     gettimeofday(&tim, NULL);
     double timing2 = tim.tv_sec+(tim.tv_usec/1000000.0);
     omp_set_num_threads(1);
     run_sim();
     gettimeofday(&tim, NULL);
     double timing3 = tim.tv_sec+(tim.tv_usec/1000000.0);

     // Output speedup
     printf("\n\nOpenMP speed-up: %.3fx (perfect scaling would give %dx)\n",(timing3-timing2)/(timing2-timing1),np);

}
