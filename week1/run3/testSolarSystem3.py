#Adding 10000 test particles between 4 and 40 AU using a random number generator and obeserving their orbits
#TODO : 
# Check new Mercury interface -- DONE
# Test for 4 planets -- DONE
# Report any problems -- DONE
import numpy
import random 
from amuse.lab import *
import math
try:
    from matplotlib import pyplot
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


# If restarting after code failure after certain point, use statements below to read in the last known conditions and comment out initialization step
# solar_system  = read_set_from_file('evolutionPlanets2.hdf5','hdf5')
# test_particles = read_set_from_file('evolutionParticles2.hdf5','hdf5')

#Creating new solar system

solar_system = new_solar_system()
test_particles = Particles(10000)

def initialize():
    solar_system.remove_particle(solar_system[1])
    solar_system.remove_particle(solar_system[1])
    solar_system.remove_particle(solar_system[1])
    solar_system.remove_particle(solar_system[1])
    solar_system.remove_particle(solar_system[5])

    test_particles.mass = 0 | units.MSun

    test_particles.radius = 2.3 | units.km
    test_particles.name = "test particles"
    initializing the positions and the velocities of the test particles
    for i in range(0,10000):
        obtaining a random position with radius between 4 AU and 40 AU
       radius = (random.random()*36 + 4) | units.AU
       theta = random.random()*2*math.pi 
        
       test_particles[i].x = (radius*math.cos(theta)).value_in(units.AU) | units.AU
       test_particles[i].y = (radius*math.sin(theta)).value_in(units.AU) | units.AU
       test_particles[i].z = 0 | units.AU
        
       velocity_squared = (constants.G * solar_system[0].mass / radius)
       velocity = math.sqrt(velocity_squared.value_in(units.km **2 / units.s **2))
       vx = -velocity*math.sin(theta)
       vy = velocity*math.cos(theta)
       test_particles[i].vx = (vx)| (units.km / units.s)
       test_particles[i].vy = (vy) | (units.km / units.s)
       test_particles[i].vz = 0 | (units.km / units.s)


def planetplot():

    mer = Mercury()
    mer.initialize_code()
    
    mer.particles.add_particle(solar_system)
    mer.particles.add_particle(test_particles)

    mer.commit_particles()


    channel = mer.particles.new_channel_to(solar_system)
    channel_to_test_particles = mer.particles.new_channel_to(test_particles)

    t_end= 100000 | units.yr
    time=0 | units.yr
    count = 0
    while time<t_end:
        time=time+ (1000 | units.yr)
        err=mer.evolve_model(time)
        
        channel.copy()
        channel_to_test_particles.copy()
        solar_system.savepoint(time)
        test_particles.savepoint(time)
        write_set_to_file(solar_system,'evolutionPlanets3.hdf5','hdf5')
        write_set_to_file(test_particles,'evolutionParticles3.hdf5','hdf5')

        print(str(count))
        count = count + 1



    mer.stop()
    
if __name__  == "__main__":
    print "this may take a while.."
    initialize()
    planetplot()
