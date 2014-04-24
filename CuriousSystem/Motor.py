from setup import *


class Motor(object):

    # lower nad upper bound of the motor accelerates
    # actually only upper bound matters
    accelBound = (-1.5, 1.0)
    angAccelBound = (-math.pi/4000, math.pi/4000)

    simpleStates = tuple(range(num_simpleStates_m))

    def __init__(self, default=[0]*2, simple=False):
        if simple:
            self.val = 0
        else:
            accel = default[0]  # velocity
            angAccel = default[1]  # angular velocity
            self.val = [accel, angAccel]

        self.simple = simple

    def getParam(self):
        return tuple(self.getVal(),)

    def getVal(self):
        return self.val

    def setVal(self, new_val):
        self.val = new_val

    def getNumParam(self):
        return len(self.getParam())

    def getBound(simple=False):
        if simple:
            return [[min(Motor.simpleStates), max(Motor.simpleStates)]]
        return [Motor.accelBound, Motor.angAccelBound]
    getBound = staticmethod(getBound)

    def getSimpleStates(self):
        if self.simple:
            return self.simpleStates
        else:
            print("Not in simple mode!")
            raise

    def isSimple(self):
        return self.simple