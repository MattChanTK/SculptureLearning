from setup import *


class Sensor():

    def __init__(self):
        self.hr = 0
        self.skin = 0
        self.interest = 0

        # Maybe add these sensor
        #self.x = 0
        #self.y = 0
        #self.dir = 0

    def getParam(self):
        return [self.hr, self.skin, self.interest]

    def getNumParam(self):
        return len(self.getParam())


