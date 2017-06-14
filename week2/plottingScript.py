from amuse.lab import *
import h5py
import math
import numpy
import sys

mu = constants.G.value_in((units.km)**3 /(units.s **2))

fileName = sys.argv[1]
f = h5py.File(fileName,'r')
vx = []
vy = []
vz = []

x = []
y = []
z = []


def orbital_elements_test_particles(xx,yy,zz,vxx,vyy,vzz):
    #Using vis-viva equation
    m = 1 
    dist = (math.sqrt(xx ** 2 + yy ** 2 + zz ** 2)) | units.AU
    v_squared = vxx ** 2 + vyy ** 2 + vzz ** 2
    
    one_over_a = 2/dist.value_in(units.AU) - ((v_squared/mu) | (1/units.km)).value_in(1/units.AU)
    a = 1/one_over_a

    x_vec = numpy.array([xx,yy,zz])
    v_vec = numpy.array([vxx,vyy,vzz])

    h_vec = numpy.cross(x_vec, v_vec)
    z_vec = [0, 0, 1]

    inc = numpy.arccos(numpy.dot(h_vec, z_vec) / (numpy.linalg.norm(h_vec) * numpy.linalg.norm(z_vec))) * 360 / (2 * math.pi)

    epsilon = ((v_squared / 2) - (mu / dist.value_in(km))) | (units.km ** 2 / units.s **2)

    ecc = math.sqrt(1+2*epsilon.value_in(units.km **2 / units.s **2)*(numpy.dot(h_vec,h_vec)*((1 | units.AU ** 2).value_in(units.km **2)))/(mu ** 2)) #let's hope this works!
    return a , ecc, inc 

def get_attributes():
    attributes = f['particles']['0000000100']['attributes']
    vx = attributes['vx']
    vy = attributes['vy']
    vz = attributes['vz']

    x = attributes['x']
    y = attributes['y']
    z = attributes['z']


def plot():
    pyplot.xlim(0,100000)
    pyplot.xscale('log')
    pyplot.ylim(0,360)
    numOfParticles = len(vx)
    for i in range(0,numOfParticles):
        if (x[i] != 0 and y[i] != 0 and z[i]!= 0):
            semi_major , ecc , inc = orbital_elements_test_particles(x[i],y[i],z[i],vx[i],vy[i],vz[i])
            pyplot.plot(semi_major,i,'ro')
        else:
            continue
    pyplot.savefig()#enternameofFile

    f.close()

if __name__ == '__main__':
    get_attributes()
    plot()

