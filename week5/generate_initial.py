import rebound
from amuse.lab import *
import random
import numpy

solar_system = new_solar_system()
semi_major = [5.5,8,14,11]
solar_system.remove(solar_system[1])    #mercury
solar_system.remove(solar_system[1])    #venus  
solar_system.remove(solar_system[1])    #earth
solar_system.remove(solar_system[1])    #mars
solar_system.remove(solar_system[5])    #pluto

#planetesimal initial conditions
disk_mass = 0.1 | units.MJupiter
number_of_planetesimals = 1000
radius_of_planetesimals = (500 | units.km).value_in(units.AU)
disk_start = 16
disk_end = 35

def convert_radius(r):
    r_i = r.value_in(units.AU)
    return r_i

def convert_velocity(v):
    return v.value_in(units.AU / units.yr)


def generate():
    #sun & four planets
    sun = solar_system[0]
    sim = rebound.Simulation()
    sim.units = ('yr','AU','Msun')
    sim.add(m=1.0,r=convert_radius(sun.radius),
        x=sun.x,y=sun.y,z=sun.z,
        vx=convert_velocity(sun.vx),vy=convert_velocity(sun.vy),vz=convert_velocity(sun.vz))

    for i in xrange(1,5):
        sim.add(m=solar_system[i].mass,a=semi_major[i-1],e=0.0,inc=0.001,f=(i*numpy.pi/4))

    sim.N_active = sim.N 

    #generating the disk of planetesimals 

    mass_of_each_planetesimal = (disk_mass/number_of_planetesimals).value_in(units.MSun)


    for i in xrange(0,number_of_planetesimals):
        sem = random.random()*(disk_end-disk_start) + disk_start
        theta = random.random()*2*numpy.pi
        sim.add(m=mass_of_each_planetesimal,r=radius_of_planetesimals,a=sem,f=theta,e=0.0,inc=0.0)

    sim.save('initial.in')

if __name__ == '__main__':
    generate()

        


