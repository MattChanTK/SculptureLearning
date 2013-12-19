__author__ = 'Matthew'


class sma_segment(object):

    cold_length = 35.0  # unit = mm
    hot_length = 34.1  # unit = mm
    warming_rate = 0.36  # unit = mm/s
    cooling_rate = 0.05  # unit = mm/s

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

