from amuse.lab import *
import h5py
import math
import numpy
import numba
import sys
from matplotlib import pyplot
mu = constants.G.value_in((units.km)**3 /(units.s **2 * units.MSun))
#fileName = sys.argv[1]
fileName = 'evolutionParticles_w2r1_nice_0.hdf5'
f = h5py.File(fileName,'r')
fS = h5py.File('evolutionSolarSystem_w2r1_nice_0.hdf5')

@numba.jit
def orbital_elements_test_particles(x,y,z,vx,vy,vz,mm,xSun,ySun,zSun,vxSun,vySun,vzSun):
    a = []
    ecc = []
    inc = []
    q = []
    for i in range(0,2000):
        #Using vis-viva equation
        m = 1 + mm[i]
        xx = xSun-x[i]
        yy = ySun - y[i]
        zz = zSun - z[i]
        vxx = vxSun - vx[i]
        vyy = vySun - vy[i]
        vzz = vzSun - vz[i]
        dist = (numpy.sqrt(xx ** 2 + yy ** 2 + zz ** 2)) | units.AU
        if (dist.value_in(units.AU) == 0):
            dist = -999999 | units.AU
        v_squared = vxx ** 2 + vyy ** 2 + vzz ** 2

        one_over_a = 2/dist.value_in(units.AU) - ((v_squared/mu) | (1/units.km)).value_in(1/units.AU)

        a_i = 1/one_over_a
        a.append(a_i)


        x_vec = numpy.array([xx,yy,zz])
        v_vec = numpy.array([vxx,vyy,vzz])

        h_vec = numpy.cross(x_vec, v_vec)
        z_vec = [0, 0, 1]

        inc_i = numpy.arccos(numpy.dot(h_vec, z_vec) / (numpy.linalg.norm(h_vec) * numpy.linalg.norm(z_vec))) * 360 / (2 * math.pi)
        inc.append(inc_i)

        epsilon = ((v_squared / 2) - (mu / dist.value_in(units.km))) | (units.km ** 2 / units.s **2)

        ecc_i = numpy.sqrt(1+2*epsilon.value_in(units.km **2 / units.s **2)*(numpy.dot(h_vec,h_vec)*((1 | units.AU ** 2).value_in(units.km **2)))/(mu ** 2)) #let's hope this works!
        ecc.append(ecc_i)

        q_i = a_i*(1-ecc_i)
        q.append(q_i)

    return a , ecc, inc , q


def plot():

    j = 1001
    while j < 1002:
        pyplot.xlim(40)

        #pyplot.xscale('log')
        pyplot.ylim(0,0.4)
        pyplot.ylabel('eccentricity')
        #pyplot.xticks([10 ** i for i in range(0,3)])
        pyplot.gca().invert_xaxis()

        pyplot.xlabel('a (AU)')

        currentTime = str(j).zfill(10)
        attributes = f['particles'][currentTime]['attributes']
        attributesSun = fS['particles'][currentTime]['attributes']
        vx = attributes['vx']
        vy = attributes['vy']
        vz = attributes['vz']

        x = attributes['x']
        y = attributes['y']
        z = attributes['z']
        name = attributes['name']
        mass = attributes['mass']

        vxSun = attributesSun['vx'][0]
        vySun = attributesSun['vy'][0]
        vzSun = attributesSun['vz'][0]
        xSun = attributesSun['x'][0]
        ySun = attributesSun['y'][0]
        zSun = attributesSun['z'][0]

        px = attributesSun['x'][1:]
        py = attributesSun['y'][1:]
        pz = attributesSun['z'][1:]
        pvx = attributesSun['vx'][1:]
        pvy = attributesSun['vy'][1:]
        pvz = attributesSun['vz'][1:]
        pm = attributesSun['mass'][1:]

        for i in range(0,4):
            semi_major , ecc , inc , q = orbital_elements_test_particles(px[i],py[i],pz[i],pvx[i],pvy[i],pvz[i],pm[i],xSun,ySun,zSun,vxSun,vySun,vzSun)
            pyplot.plot(semi_major,ecc,'b^',markersize=12)
            print semi_major


        semi_major , ecc , inc,q = orbital_elements_test_particles(x,y,z,vx,vy,vz,0,xSun,ySun,zSun,vxSun,vySun,vzSun)


        pyplot.plot(semi_major,ecc,'r.',alpha=0.5)



        pyplot.savefig('ecc_nice_1_new_'+str(j).zfill(4)+'.png')
        j+=100
        pyplot.clf()
    f.close()
    fS.close()
if __name__ == '__main__':
    print "plotting..."
    plot()

