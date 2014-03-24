from setup import *


class Sensor(object):

    # lower nad upper bound of the sensor values
    hrBound = [0.0, 200.0]
    skinBound = [0.0, 5.0]
    interestBound = [0.0, 1.0]

    def __init__(self, default=[0]*3):
        self.hr = default[0]
        self.skin = default[1]
        self.interest = default[2]

    def getParam(self):
        return [self.hr, self.skin, self.interest]

    def getNumParam(self):
        return len(self.getParam())

    def getBound():
        return [Sensor.hrBound, Sensor.skinBound, Sensor.interestBound]
    getBound = staticmethod(getBound)


