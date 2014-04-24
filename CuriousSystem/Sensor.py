from setup import *


class Sensor(object):

    # lower nad upper bound of the sensor values
    hrBound = (0.0, 1.0)
    skinBound = (0.0, 1.0)
    interestBound = (0.0, 1.0)

    simpleStates = tuple(range(num_simpleStates_s))


    def __init__(self, default=[0]*3, simple=False):
        if simple:
            self.val = 0
        else:
            hr = default[0]
            skin = default[1]
            interest = default[2]
            self.val = [hr, skin, interest]

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
            return [min(Sensor.simpleStates), max(Sensor.simpleStates)]
        return (Sensor.hrBound, Sensor.skinBound, Sensor.interestBound)
    getBound = staticmethod(getBound)

    def getSimpleStates():
        return Sensor.simpleStates
    getSimpleStates = staticmethod(getSimpleStates)

    def isSimple(self):
        return self.simple



