from setup import *
import random
import Sensor

class Simson:
    def __init__(self):
        self.hr = 0.8
        self.skin = 0.5
        self.interest = 0.0

        self.k_hr = 1 #2
        self.k_skin = 1 #0.005
        self.k_interest = 1

    def react(self, feature):
        bounds = Sensor.Sensor.getBound()
        self.hr = max(bounds[0][0], min(bounds[0][1], self.k_hr*feature[0])) #+ random.random() * 60 - 30
        self.skin = max(bounds[1][0], min(bounds[1][1], self.k_skin*feature[1])) #+ random.random() * 1 - 0.5
        self.interest = max(bounds[2][0], min(bounds[2][1], self.k_interest*feature[2])) # + random.random() * 0.8 -0.4