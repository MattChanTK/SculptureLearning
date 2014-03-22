from setup import *
import random

class Simson:
    def __init__(self):
        self.hr = 80
        self.skin = 1.2
        self.interest = 0.5

        self.k_hr = 8
        self.k_skin = 0.01
        self.k_interest = 0.1

    def react(self, feature):
        self.hr = self.k_hr*feature[0] + random.random() * 60 - 30
        self.skin = self.k_skin*feature[1] + random.random() * 1 - 0.5
        self.interest = self.k_interest*feature[2] + random.random() * 0.8 -0.4