from setup import *


class Motor(object):

    # lower nad upper bound of the motor accelerates
    # actually only upper bound matters
    accelBound = (-2.0, 2.0)
    angAccelBound = (-math.pi/4000, math.pi/4000)

    simpleStates = tuple(range(num_simpleStates_m))

    def __init__(self, val=[0]*2, simple=False):
        if simple:
            self.val = val[0]
        else:
            accel = val[0]  # velocity
            angAccel = val[1]  # angular velocity
            self.val = [accel, angAccel]

        self.simple = simple

    def getParam(self):
        if self.isSimple():
            return (self.getVal(),)
        return tuple(self.getVal())

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

    def getSimpleStates():
        return Motor.simpleStates
    getSimpleStates = staticmethod(getSimpleStates)

    def isSimple(self):
        return self.simple