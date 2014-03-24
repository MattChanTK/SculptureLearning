from setup import *


class Sensor():

    def __init__(self, default=[0]*3):
        self.hr = default[0]
        self.skin = default[1]
        self.interest = default[2]

        # lower nad upper bound of the sensor values
        self.hrBound = [0.0, 200.0]
        self.skinBound = [0.0, 5.0]
        self.interestBound = [0.0, 1.0]

    def getParam(self):
        return [self.hr, self.skin, self.interest]

    def getNumParam(self):
        return len(self.getParam())

    def getBound(self):
        return [self.hrBound, self.skinBound, self.interestBound]



