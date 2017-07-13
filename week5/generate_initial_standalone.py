import rebound
from amuse.lab import *
import random
import numpy


#parameter space
delta_a_u = [-0.2,-0.1,0.1,0.2]
delta_a_n = [-0.2,-0.1,0.1,0.2]
delta_a_j = [-0.1,0.1]
delta_a_s = [-0.1,0.1]

solar_system = new_solar_system()

solar_system.remove_particle(solar_system[1])    #mercury
solar_system.remove_particle(solar_system[1])    #venus
solar_system.remove_particle(solar_system[1])    #earth
solar_system.remove_particle(solar_system[1])    #mars
solar_system.remove_particle(solar_system[5])    #pluto

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
    for dau in delta_a_u:
        for dan in delta_a_n:
            for das in delta_a_s:
                for daj in delta_a_j:
                    semi_major = [5.5+daj,8+das,14+dau,11+dan]

                    sun = solar_system[0]
                    sim = rebound.Simulation()
                    sim.units = ('yr','AU','Msun')
                    sim.add(m=1.0,r=convert_radius(sun.radius),
                        x=sun.x.value_in(units.AU),y=sun.y.value_in(units.AU),z=sun.z.value_in(units.AU),
                        vx=convert_velocity(sun.vx),vy=convert_velocity(sun.vy),vz=convert_velocity(sun.vz))


                    for i in xrange(1,5):
                        sim.add(m=solar_system[i].mass.value_in(units.MSun),a=semi_major[i-1],e=0.0,inc=0.001,f=(i*numpy.pi/4))

                    sim.N_active = sim.N

                    for i in xrange(0,number_of_particles):
                        semi_major = (random.random()*(disk_end-disk_start) + disk_start)
                        theta = random.random()*2*math.pi
                        sim.add(m=mass_of_particle,r=radius_of_particles,a=semi_major,e=0.0,inc=0.0,f=theta)

                    sim.move_to_com()

                    sim.save('initial_j_'+str(daj)+'_s_'+str(das)+'_n_'+str(dan)+'_u_'+str(dau)+'.in')

if __name__ == '__main__':
    generate()




