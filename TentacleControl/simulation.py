__author__ = 'Matthew'
import Tentacle

# simulation parameters
num_step = 100
sim_step = 0.01

# instantiating the Tentacle
plant = Tentacle.Tentacle()

print 'initial angle: %f' % plant.get_angle()

for t in range(num_step):
    plant.update(1, sim_step=sim_step)
    print '[%4d] angle: %f' % (t+1, plant.get_angle())






