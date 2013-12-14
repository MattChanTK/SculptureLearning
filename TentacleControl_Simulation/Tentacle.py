__author__ = 'Matthew'

import math
import sma_array as sa
import sma_segment as ss

class Tentacle(object):

    # length of lever arm
    r = 20  # unit = mm

    # saturation values
    min_input = 0

    def __init__(self, num_seg=10):

        # instance parameters
        self.array = sa.sma_array(num_seg=num_seg)
        self.array.set_all_off()
        #total length of SMA at 90 degree (neutral)
        self.L0 = (ss.sma_segment.hot_length + ss.sma_segment.cold_length)*(num_seg/2)

        # Tentacle parameters
        Tentacle.max_input = num_seg
        Tentacle.r = self.array.get_length_range()/(2*math.cos(math.radians(60)))


    def get_angle(self, deg=True):
        angle = math.acos((self.L0-self.array.get_total_length())/Tentacle.r)

        if deg:
            return math.degrees(angle)
        else:
            return angle


    def update(self, input_val, num_step=1, sim_step=0.01):
        if input_val < Tentacle.min_input:
            input_val = Tentacle.min_input
        elif input_val > Tentacle.max_input:
            input_val = Tentacle.max_input

        self.array.turn_on(input_val, num_step=num_step, sim_step=sim_step)


