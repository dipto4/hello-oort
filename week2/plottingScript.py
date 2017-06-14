from amuse.lab import *
import h5py
import math
import numpy
import sys

mu = constants.G.value_in((units.km)**3 /(units.MSun * units.s **2))





def orbital_elements_test_particles(xx,yy,zz,vxx,vyy,vzz):
    #Using vis-viva equation
    m = 1 
    dist = math.sqrt(xx ** 2 + yy ** 2 + zz ** 2)
    v_squared = vxx ** 2 + vyy ** 2 + vzz ** 2
    
    one_over_a = 2/dist - ((v_squared/mu) | (1/units.km)).value_in(1/units.AU)
    a = 1/one_over_a

    x_vec = numpy.array([xx,yy,zz])
    v_vec = numpy.array([vxx,vyy,vzz])

    h_vec = numpy.cross(x_vec, v_vec)
    z_vec = [0, 0, 1]

    inc = numpy.arccos(numpy.dot(h_vec, z_vec) / (numpy.linalg.norm(h_vec) * numpy.linalg.norm(z_vec))) * 360 / (2 * math.pi)

    epsilon = (v_squared / 2) - (mu / dist) # change units

    ecc = math.sqrt(1+2*epsilon*numpy.dot(h_vec,h_vec)/(mu ** 2))

    return a , ecc, inc 

f = h5py.File('solartest.hdf5','r')

attributes = f['particles']['0000000100']['attributes']
vx = attributes['vx']
vy = attributes['vy']
vz = attributes['vz']

x = attributes['x']
y = attributes['y']
z = attributes['z']

for i in range(0,9):
	a , ecc , inc = orbital_elements_test_particles(x[i],y[i],z[i],vx[i],vy[i],vz[i])
	print a , inc 
f.close()

