from setup import *


class Sensor(object):


    # lower nad upper bound of the sensor values
    hrBound = (0.0, 1.0)
    skinBound = (0.0, 1.0)
    interestBound = (0.0, 1.0)
    vBound = (0.0, 400.0)
    wBound = (0.0, 0.1)
    xBound = (0.0, 900.0)
    yBound = (0.0, 600.0)
    dirBound = (-math.pi, math.pi)

    # simple state
    simpleStates = tuple(range(num_simpleStates_s))


    def __init__(self, val=[0]*8, simple=False):

        if simple:
            self.val = val[0]
        else:

            hr = val[0]
            skin = val[1]
            interest = val[2]
            v = val[3]
            w = val[4]
            x = val[5]
            y = val[6]
            dir = val[7]

            self.val = [hr, skin, interest, v, w, x, y, dir]

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
        return (Sensor.hrBound, Sensor.skinBound, Sensor.interestBound,
                Sensor.vBound, Sensor.wBound,
                Sensor.xBound, Sensor.yBound, Sensor.dirBound)
    getBound = staticmethod(getBound)

    def getSimpleStates():
        return Sensor.simpleStates
    getSimpleStates = staticmethod(getSimpleStates)

    def isSimple(self):
        return self.simple



