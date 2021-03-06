#Adding 1000 test particles between 4 and 40 AU using a random number generator and obeserving their orbits
#TODO:
#1. Add units
#2. Add more particles
#3. Increase timestep
#4. Intermediate step plot
#5. Increase time duration
import numpy
import random 
from amuse.lab import *
import math
try:
    from matplotlib import pyplot
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

solarsystem= \
 [['JUPITER',9.54791938424326609E-04,3.,1.33, \
  4.84143144246472090E+00, -1.16032004402742839E+00, -1.03622044471123109E-01, \
  1.66007664274403694E-03,  7.69901118419740425E-03, -6.90460016972063023E-05, \
  0., 0., 0.],
 ['SATURN',2.85885980666130812E-04,3.,0.70, \
  8.34336671824457987E+00,  4.12479856412430479E+00, -4.03523417114321381E-01, \
 -2.76742510726862411E-03,  4.99852801234917238E-03,  2.30417297573763929E-05, \
  0., 0., 0.],
 ['URANUS',4.36624404335156298E-05,3.,1.30, \
  1.28943695621391310E+01, -1.51111514016986312E+01, -2.23307578892655734E-01, \
  2.96460137564761618E-03,  2.37847173959480950E-03, -2.96589568540237556E-05, \
  0., 0., 0.],
 ['NEPTUNE',5.15138902046611451E-05,3.,1.76, \
  1.53796971148509165E+01, -2.59193146099879641E+01,  1.79258772950371181E-01, \
  2.68067772490389322E-03,  1.62824170038242295E-03, -9.51592254519715870E-05, \
  0., 0., 0.]]

#Adding test particles

test_particles = Particles(1000)

mass_of_particle = 0 

density_of_particle = 0 /((4/3)*constants.pi*(2300e2)**3) 
test_particles.celimit = 0.
test_particles.density = density_of_particle
test_particles.mass = mass_of_particle
test_particles.Lx = 0
test_particles.Ly = 0
test_particles.Lz = 0.

#initializing the positions and the velocities of the test particles
for i in range(0,1000):
    #obtaining a random position with radius between 4 AU and 40 AU
    radius = random.random()*36 + 4
    theta = random.random()*2*math.pi 
    
    test_particles[i].xpos = radius*math.cos(theta)
    test_particles[i].ypos = radius*math.sin(theta)
    test_particles[i].zpos = 0
    

    velocity = math.sqrt(constants.G.value_in((units.AU **3)/(units.MSun * units.day **2))/(radius))
    vx = velocity*math.sin(theta)
    vy = velocity*math.cos(theta)
    test_particles[i].vx = vx
    test_particles[i].vy = vy
    test_particles[i].vz = 0


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


def planetplot():
    instance=MercuryInterface()
    instance.initialize_code()
    ids=dict()
    xpos=dict()
    ypos=dict()
    zpos=dict()
    tvx = dict()
    tvy = dict()
    tvz = dict()
    mm = dict()
    for x in solarsystem:
        pid,err=instance.new_orbiter(x[1],x[3],
         x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[2])
        ids[x[0]]=pid
        xpos[x[0]]=[]
        ypos[x[0]]=[]
        xpos[x[0]].append(x[4])
        ypos[x[0]].append(x[5])

    instance.commit_particles()

    for p in test_particles:
        pid,err = instance.new_orbiter(p.mass,p.density,p.xpos,p.ypos,p.zpos,p.vx,p.vy,p.vz,p.celimit,p.Lx,p.Ly,p.Lz)
        ids[p] = pid
        #xpos[p] = []
        #ypos[p] = []
        xpos[p] = p.xpos
        ypos[p] = p.ypos
        zpos[p] = p.zpos
        tvx[p] = p.vx 
        tvy[p] = p.vy
        tvz[p] = p.vz 

    instance.commit_particles()

    pyplot.plot(xpos['JUPITER'],ypos['JUPITER'])
    pyplot.plot(xpos['SATURN'],ypos['SATURN'])
    pyplot.plot(xpos['URANUS'],ypos['URANUS'])
    pyplot.plot(xpos['NEPTUNE'],ypos['NEPTUNE'])
    for t in test_particles:
        pyplot.plot([xpos[t]],[ypos[t]],'bo')
    pyplot.xlim(-100.0, 100.0)
    pyplot.ylim(-100.0, 100.0)
    pyplot.savefig('solarsytemstart2.png')
    pyplot.clf()
    print "wow so pyplot very headache much oort"
    for t in test_particles:
        semi_major , ec, i = orbital_elements_test_particles(-xpos[t],-ypos[t],-zpos[t],-tvx[t],-tvy[t],-tvz[t])

        pyplot.xlim(0,100)
        pyplot.ylim(0,360)

        pyplot.plot(semi_major,i,'ro')
        pyplot.savefig('incinitial.png')
    pyplot.clf()


    t_end=365.25*1e6
    time=0
    count = 0
    while time<t_end:
        time=time+365.25*1000
        err=instance.evolve_model(time)
        for p in solarsystem:
            mass,dens,x,y,z,vx,vy,vz,sx,sy,sz,celimit,err=  \
              instance.get_orbiter_state(ids[p[0]])
            xpos[p[0]].append(x)
            ypos[p[0]].append(y)
        for t in test_particles:
            t_mass,t_dens,t_x,t_y,t_z,t_vx,t_vy,t_vz,t_sx,t_sy,t_sz,t_celimit,err= \
              instance.get_orbiter_state(ids[t])
            xpos[t] = t_x
            ypos[t] = t_y
            zpos[t] = t_z
            tvx[t] = t_vx
            tvy[t] = t_vy
            tvz[t] = t_vz
                

        if (time >= 5e5*365 and time < 5.001e5*365.25):
            pyplot.plot(xpos['JUPITER'],ypos['JUPITER'])
            pyplot.plot(xpos['SATURN'],ypos['SATURN'])
            pyplot.plot(xpos['URANUS'],ypos['URANUS'])
            pyplot.plot(xpos['NEPTUNE'],ypos['NEPTUNE'])
            for t in test_particles:
                pyplot.plot(xpos[t],ypos[t])
            pyplot.xlim(-500.0, 500.0)
            pyplot.ylim(-500.0, 500.0)
            pyplot.savefig('solarsytem'+str(time)+'.png')
            print "wow so pyplot very headache much oort"
            pyplot.clf()
            for t in test_particles:
                semi_major , ec, i = orbital_elements_test_particles(-xpos[t],-ypos[t],-zpos[t],-tvx[t],-tvy[t],-tvz[t])

                pyplot.xlim(0,5000)
                pyplot.ylim(0,360)

                pyplot.plot(semi_major,i,'ro')
                pyplot.savefig('incinter'+str(time)+'.png')
            pyplot.clf()

        print(str(count))
        count = count + 1

    pyplot.plot(xpos['JUPITER'],ypos['JUPITER'])
    pyplot.plot(xpos['SATURN'],ypos['SATURN'])
    pyplot.plot(xpos['URANUS'],ypos['URANUS'])
    pyplot.plot(xpos['NEPTUNE'],ypos['NEPTUNE'])
    for t in test_particles:
        pyplot.plot(xpos[t],ypos[t])
    pyplot.xlim(-10000.0, 10000.0)
    pyplot.ylim(-10000.0, 10000.0)
    pyplot.savefig('solarsytem'+str(time)+'.png')
    print "wow so pyplot very headache much oort"
    pyplot.clf()

    for t in test_particles:
        semi_major , ec, i = orbital_elements_test_particles(-xpos[t],-ypos[t],-zpos[t],-tvx[t],-tvy[t],-tvz[t])

        pyplot.xlim(0,10000)
        pyplot.ylim(0,360)

        pyplot.plot(semi_major,i,'ro')
        pyplot.savefig('incfinal.png')
    pyplot.clf()
    instance.stop()
    


if __name__  == "__main__":
    print "this may take a while.."
    planetplot()
