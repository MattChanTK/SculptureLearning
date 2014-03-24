from setup import *


class Motor(object):

    # lower nad upper bound of the motor values
    vBound = [-200.0, 200.0]
    wBound = [-math.pi, math.pi]

    def __init__(self, default=[0, 0]):
        self.v = default[0]  # velocity
        self.w = default[1]  # angular velocity

    def getParam(self):
        return [self.v, self.w]

    def getNumParam(self):
        return len(self.getParam())

    def getBound():
        return [Motor.vBound, Motor.wBound]
    getBound = staticmethod(getBound)
