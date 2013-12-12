__author__ = 'Matthew'

import math
import sma_array as sa
import sma_segment as ss

class Tentacle(object):

    # length of lever arm
    r = 20 # unit = mm

    def __init__(self, num_seg=10):
        self.array = sa.sma_array(num_seg=num_seg)
        self.array.set_all_off()
        #total length of SMA at 90 degree (neutral)
        self.L0 = (ss.sma_segment.hot_length + ss.sma_segment.cold_length)*(num_seg/2)


    def get_angle(self, deg=True):
        angle = math.acos((self.array.get_total_length()-self.L0)/Tentacle.r)

        if deg:
            return math.degrees(angle)
        else:
            return angle


    def update(self, input, num_step=1, sim_step=0.01):
        self.array.turn_on(input, num_step=num_step, sim_step=sim_step)


