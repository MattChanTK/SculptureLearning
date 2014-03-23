from setup import *


class Sensor():

    def __init__(self, default=[0]*3):
        self.hr = default[0]
        self.skin = default[1]
        self.interest = default[2]

        # Maybe add these sensor
        #self.x = 0
        #self.y = 0
        #self.dir = 0

    def getParam(self):
        return [self.hr, self.skin, self.interest]

    def getNumParam(self):
        return len(self.getParam())


