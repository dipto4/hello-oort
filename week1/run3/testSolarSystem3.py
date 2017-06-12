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
#Creating new solar system

solar_system = new_solar_system()
solar_system.remove_particle(solar_system[1])
solar_system.remove_particle(solar_system[1])
solar_system.remove_particle(solar_system[1])
solar_system.remove_particle(solar_system[1])
solar_system.remove_particle(solar_system[5])

#Adding test particles

test_particles = Particles(10000)

test_particles.mass = 0 | units.MSun

test_particles.radius = 0 | units.RSun

#initializing the positions and the velocities of the test particles
for i in range(0,10000):
    #obtaining a random position with radius between 4 AU and 40 AU
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

'''
def orbital_elements_test_particles(xx,yy,zz,vxx,vyy,vzz):
    #Using vis-viva equation
    m = 1 
    dist = math.sqrt(xx ** 2 + yy ** 2 + zz ** 2)
    v_squared = vxx ** 2 + vyy ** 2 + vzz ** 2
    mu = constants.G.value_in((units.AU **3)/(units.MSun * units.day **2))
    one_over_a = 2/dist - v_squared/mu
    a = 1/one_over_a

    x_vec = numpy.array([xx,yy,zz])
    v_vec = numpy.array([vxx,vyy,vzz])

    h_vec = numpy.cross(x_vec, v_vec)
    z_vec = [0, 0, 1]

    inc = numpy.arccos(numpy.dot(h_vec, z_vec) / (numpy.linalg.norm(h_vec) * numpy.linalg.norm(z_vec))) * 360 / (2 * math.pi)

    ecc = math.sqrt(1-(numpy.dot(h_vec,h_vec))/(mu*a))

    return a , ecc, inc 
'''

def planetplot():

    mer = Mercury()
    mer.initialize_code()
    
    mer.particles.add_particle(solar_system)
    mer.particles.add_particle(test_particles)

    mer.commit_particles()

    print mer.particles

    channel = mer.particles.new_channel_to(solar_system)
    channel_to_test_particles = mer.particles.new_channel_to(test_particles)

    t_end= 1e6 | units.yr
    time=0 | units.yr
    count = 0
    while time<t_end:
        time=time+ (1000 | units.yr)
        err=mer.evolve_model(time)
        
        channel.copy()
        channel_to_test_particles.copy()
        solar_system.savepoint(time)
        test_particles.savepoint(time)
        write_set_to_file(solar_system,'evolutionPlanets.hdf5','hdf5')
        write_set_to_file(test_particles,'evolutionParticles.hdf5','hdf5')

        print(str(count))
        count = count + 1


    print mer.particles

    mer.stop()
    


if __name__  == "__main__":
    print "this may take a while.."
    planetplot()
