LEAPS 2017 code

Week 1 : Putting a collection of test particles at random locations between 4 AUand 40 AU from the sun thereby forming a disk.
Particles are initially in a circular orbit with zero inclination and eccentricity.Velocity of the particles was found using the formula for centrifugal force.

Week 2 : Running code with Mercury() instead of MercuryInterface() posed a problem which has been taken care of. Code has been made 
more concise and modular. Data is being stored in hdf5 files instead of plotting them directly. Please see week folder for more details. Different initial conditions based on the nice model have been followed.

Week 3: Running nice model simulations upto 10 Myr. Improved plotting scripts. Using colorbars.

Week 4: Simulations with particles with mass instead of test particles. Configuration similar to Nice model configurations. Mass of disk = 0.1 M_Jupiter.
Radius of particles ~ radius of pluto. Number of particles = 2000


NOTE: Use the new version of AMUSE instead of the binary release.
Usage with MPICH2: 

mpiexec.hydra -n 1 amuse.sh nameOfScript.py


