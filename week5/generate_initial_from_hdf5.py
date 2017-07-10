'''
HDF5 Files were written using AMUSE. Units used by the HDF5 file are as follows:
x,y,z = AU
mass = MSun
Radius = RSun
vx,vy,vz = km/s
'''

import rebound
from amuse.units import units
import os

filename = "" #enter hdf5 file here
completeFilePath = os.getcwd()+'/' + filename
fS = h5py.File(completeFilePath,'r')

number_of_particles = 1000
radius_of_particles = (500 | units.km).value_in(units.AU)
disk_start = 16
disk_end = 35
disk_mass = (0.1 | units.MJupiter).value_in(units.MSun)


def convert_v(v):
	v_i = v | (units.km / unit.s)
	return v_i.value_in(units.AU/units.yr)

def convert_radius(r):
	r_i = r | (units.RSun)
	return r_i.value_in(units.AU)

def generate():
	sim = rebound.Simulation()
	reb.units = ('yr','AU','Msun')

	currentTime = str(242001).zfill(10)

	attributes_ss = fS['particles'][currentTime]['attributes']

    for i in range(0,5):
        vx_i = convert_vel(attributes_ss['vx'][i])
        vy_i = convert_vel(attributes_ss['vy'][i])
        vz_i = convert_vel(attributes_ss['vz'][i])
        r_i = convert_radius(attributes_ss['radius'][i])

        sim.add(m=attributes_ss['mass'][i],r=r_i,x=attributes_ss['x'][i],y=attributes_ss['y'][i],z=attributes_ss['z'][i],vx=vx_i,vy=vy_i,vz=vz_i)

    sim.N_active = sim.N
    sim.move_to_com()
    mass_of_particle = disk_mass / number_of_particles
    for i in xrange(0,number_of_particles):
        semi_major = (random.random()*(disk_end-disk_start) + disk_start)
        theta = random.random()*2*math.pi
        sim.add(m=mass_of_particle,r=radius_of_particles,a=semi_major,e=0.0,inc=0.0,f=theta)

    sim.move_to_com()

    sim.save('initial.in')

if __name__ == '__main__':
	generate()




