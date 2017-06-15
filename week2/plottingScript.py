from amuse.lab import *
import h5py
import math
import numpy
import sys
from matplotlib import pyplot
mu = constants.G.value_in((units.km)**3 /(units.s **2 * units.MSun))
#fileName = sys.argv[1]
fileName = 'evolutionParticles_w2r1_0.hdf5'
f = h5py.File(fileName,'r')
fS = h5py.File('evolutionSolarSystem_w2r1_0.hdf5')

attributes = f['particles']['0000001000']['attributes']
attributesSun = fS['particles']['0000001000']['attributes']
vx = attributes['vx']
vy = attributes['vy']
vz = attributes['vz']

x = attributes['x']
y = attributes['y']
z = attributes['z']

mass = attributes['mass']

vxSun = attributesSun['vx'][0]
vySun = attributesSun['vy'][0]
vzSun = attributesSun['vz'][0]
xSun = attributesSun['x'][0]
ySun = attributesSun['y'][0]
zSun = attributesSun['z'][0]




def orbital_elements_test_particles(xx,yy,zz,vxx,vyy,vzz,m):
    #Using vis-viva equation
    m = 1 
    xx = xSun-xx
    yy = ySun - yy
    zz = zSun - zz
    vxx = vxSun - vxx
    vyy = vySun - vyy
    vzz = vzSun - vzz
    dist = (math.sqrt(xx ** 2 + yy ** 2 + zz ** 2)) | units.AU
    if (dist.value_in(units.AU) == 0):
        dist = -999999 | units.AU
    v_squared = vxx ** 2 + vyy ** 2 + vzz ** 2
    
    one_over_a = 2/dist.value_in(units.AU) - ((v_squared/mu) | (1/units.km)).value_in(1/units.AU)
    
    a = 1/one_over_a
    
    x_vec = numpy.array([xx,yy,zz])
    v_vec = numpy.array([vxx,vyy,vzz])

    h_vec = numpy.cross(x_vec, v_vec)
    z_vec = [0, 0, 1]

    inc = numpy.arccos(numpy.dot(h_vec, z_vec) / (numpy.linalg.norm(h_vec) * numpy.linalg.norm(z_vec))) * 360 / (2 * math.pi)

    epsilon = ((v_squared / 2) - (mu / dist.value_in(units.km))) | (units.km ** 2 / units.s **2)

    ecc = math.sqrt(1+2*epsilon.value_in(units.km **2 / units.s **2)*(numpy.dot(h_vec,h_vec)*((1 | units.AU ** 2).value_in(units.km **2)))/(mu ** 2)) #let's hope this works!
    
    return a , ecc, inc 


def plot():
    pyplot.xlim(100000)
    pyplot.xscale('log')
    pyplot.ylim(0,15)
    pyplot.xticks([10 ** i for i in range(-3,7)])
    pyplot.xlabel('a')
    pyplot.ylabel('e')
    pyplot.gca().invert_xaxis()
    #numOfParticles = 5
    count = 1
    for i in range(0,2000):
        
        if (x[i] != 0 and y[i] != 0 and z[i] != 0 and vx[i]!= 0 and vy[i]!= 0 and vz[i]!=0): 
            semi_major , ecc , inc = orbital_elements_test_particles(x[i],y[i],z[i],vx[i],vy[i],vz[i],mass[i])
            #print semi_major, inc, ecc
            pyplot.plot(semi_major,ecc,'ro')
            count += 1
        else:
            count+= 1
            continue

        print ecc  


    pyplot.savefig('eccinter2000_12.png')#enternameofFile

    f.close()
    fS.close()
if __name__ == '__main__':
    print "plotting..."
    plot()

