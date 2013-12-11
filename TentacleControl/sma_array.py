__author__ = 'Matthew'

import sma_segment as seg


class sma_array:


    def __init__(self, num_seg=10):
        self.array = [seg.sma_segment() for i in range(num_seg)]

    def get_num_seg(self):
        return len(self.array)



ss = sma_array()

print(ss.get_num_seg())