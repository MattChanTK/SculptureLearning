from setup import *


class Motor(object):

    # lower nad upper bound of the motor accelerates
    accelBound = [-1.5, 1.5]
    angAccelBound = [-math.pi/4000, math.pi/4000]

    def __init__(self, default=[0, 0]):
        self.accel = default[0]  # velocity
        self.angAccel = default[1]  # angular velocity

    def getParam(self):
        return [self.accel, self.angAccel]

    def getNumParam(self):
        return len(self.getParam())

    def getBound():
        return [Motor.accelBound, Motor.angAccelBound]
    getBound = staticmethod(getBound)
