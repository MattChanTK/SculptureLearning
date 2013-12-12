__author__ = 'Matthew'


class sma_segment(object):

    cold_length = 20.0  # unit = mm
    hot_length = 18.0  # unit = mm
    warming_rate = 10.0  # unit = mm/s
    cooling_rate = 6.0  # unit = mm/s

    def __init__(self):
        self.length = sma_segment.cold_length

    def activate(self, duration):
        self.length -= sma_segment.warming_rate*duration

        if self.length <= sma_segment.hot_length:
            self.length = sma_segment.hot_length

    def deactivate(self, duration):
        self.length += sma_segment.cooling_rate*duration

        if self.length >= sma_segment.cold_length:
            self.length = sma_segment.cold_length

    def set_steady_hot(self):
        self.length = sma_segment.hot_length

    def set_steady_cold(self):
        self.length = sma_segment.cold_length

