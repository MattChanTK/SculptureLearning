__author__ = 'Matthew'

import sma_segment as seg
#import math

class sma_array(object):

    def __init__(self, num_seg=10):
        self.array = [seg.sma_segment() for i in range(num_seg)]

    def get_num_seg(self):
        return len(self.array)

    def get_total_length(self):
        length = 0
        for i in range(self.get_num_seg()):
            length += self.array[i].length
        return length

    def get_length_range(self):
        max_length = seg.sma_segment.cold_length*self.get_num_seg()
        min_length = seg.sma_segment.hot_length*self.get_num_seg()

        return max_length-min_length

    def turn_on(self, num_on, num_step, sim_step=0.01):
        if num_on > self.get_num_seg():
            num_on = self.get_num_seg()

        for t in range(num_step):
            for i in range(0, num_on):
                self.array[i].activate(duration=sim_step)
            for j in range(num_on, self.get_num_seg()):
                self.array[j].deactivate(duration=sim_step)

    def set_all_off(self):

        for i in range(self.get_num_seg()):
            self.array[i].set_steady_cold()

    def set_all_on(self):

        for i in range(self.get_num_seg()):
            self.array[i].set_steady_hot()

    def set_on(self, num_on):
        if num_on > self.get_num_seg():
            num_on = self.get_num_seg()

        for i in range(0, num_on):
            self.array[i].set_steady_hot()
        for j in range(num_on, self.get_num_seg()):
            self.array[j].set_steady_cold()







