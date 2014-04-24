from setup import *
import random
import Sensor

class Simson:
    def __init__(self, simple=False):

        if simple:
            self.state = 0
        else:
            hr = 0.8
            skin = 0.5
            interest = 0.0
            self.state = [hr, skin, interest]


        self.simple = simple

    def react(self, feature):
        bounds = Sensor.Sensor.getBound()
        if self.simple:
            self.state = max(bounds[0], min(bounds[1], feature))
        else:
            hr = max(bounds[0][0], min(bounds[0][1], feature[0])) #+ random.random() * 60 - 30
            skin = max(bounds[1][0], min(bounds[1][1], feature[1])) #+ random.random() * 1 - 0.5
            interest = max(bounds[2][0], min(bounds[2][1], feature[2])) # + random.random() * 0.8 -0.4
            self.state = [hr, skin, interest]

    def setFea(self, feature):
        if self.simple:
            self.state = feature
        else:
            hr = feature[0]
            skin = feature[1]
            interest = feature[2]
            self.state = [hr, skin, interest]


    def getState(self):
        return self.state