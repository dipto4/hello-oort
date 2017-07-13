import rebound
from amuse.lab import *
import random
import numpy
from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options]",version="%prog 1.0")

parser.add_option('-u', '--uranus', action='store',dest='daus',default=0.0,help='Change in position of uranus')
parser.add_option('-n', '--neptune', action='store',dest='dans',default=0.0,help="Change in position of neptune")
parser.add_option('-j', '--jupiter', action='store',dest='dajs',default=0.0,help="Change in position of jupiter")
parser.add_option('-s', '--saturn', action='store',dest='dass',default=0.0,help="Change in position of saturn")

(option , args) = parser.parse_args()

dau = float(option.daus)
dan = float(option.dans)
daj = float(option.dajs)
das = float(option.dass)

solar_system = new_solar_system()
semi_major = [5.5+daj,8+das,14+dau,11+dan]
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
    #sun & four planets
    sun = solar_system[0]
    sim = rebound.Simulation()
    sim.units = ('yr','AU','Msun')
    sim.add(m=1.0,r=convert_radius(sun.radius),
        x=sun.x.value_in(units.AU),y=sun.y.value_in(units.AU),z=sun.z.value_in(units.AU),
        vx=convert_velocity(sun.vx),vy=convert_velocity(sun.vy),vz=convert_velocity(sun.vz))

    for i in xrange(1,5):
        sim.add(m=solar_system[i].mass.value_in(units.MSun),a=semi_major[i-1],e=0.0,inc=0.001,f=(i*numpy.pi/4))

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




