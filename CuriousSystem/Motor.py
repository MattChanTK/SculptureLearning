from setup import *


class Motor():

    def __init__(self, default=[0, 0]):
        self.v = default[0]  # velocity
        self.w = default[1]  # angular velocity

    def getParam(self):
        return [self.v, self.w]

    def getNumParam(self):
        return len(self.getParam())
