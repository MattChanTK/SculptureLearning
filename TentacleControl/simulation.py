__author__ = 'Matthew'

import math
import Tentacle
# Pyplot is a module within the matplotlib library for plotting
from matplotlib import pyplot as plt

# simulation parameters
num_step = 1200
sim_step = 0.01

# instantiating the Tentacle
plant = Tentacle.Tentacle(num_seg=14)
print 'initial angle: %f' % plant.get_angle()

# set desired angle
#ang_ref = 120
neutral_ang = 90
ang_amplitude = 30
ref_freq = 0.01
ang_ref = neutral_ang

# controller parameter
kp = -3
kd = 0.8
ki = -0.01

w0 = 0
err_sum = 0
err_0 = 0

# array of angles for plotting purposes
ang_t = [plant.get_angle()]
ang_ref_t = [ang_ref]

for t in range(num_step):

    # angle error
    error_ang = ang_ref - plant.get_angle()
    # differential error
    error_change = error_ang - err_0
    # steady state error
    err_sum += error_ang

    # save error from this iteration for the next
    err_0 = error_ang

    input_val = int(round(kp*error_ang + kd*error_change + ki*err_sum))
    plant.update(input_val, sim_step=sim_step)
    print '[%4d] angle: %7.4f     errors: %8.4f, %8.4f     input: %2d' % (t+1, plant.get_angle(), error_ang, error_change, input_val)

    ang_t.append(plant.get_angle())
    ang_ref_t.append((ang_ref))

    #if (math.fabs(error_ang) < 1):
    #    ang_ref -= 5
    #    if ang_ref < 60:
    #       ang_ref = 60
    ang_ref = ang_amplitude*math.sin(ref_freq*t) + neutral_ang

# plotting
plt.clf()
plt.ion()
time_label = [step*sim_step for step in range(0, num_step+1)]
plt.plot(time_label, ang_t)
plt.plot(time_label, ang_ref_t)
#plt.ioff()
plt.show(block=True)


