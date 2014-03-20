from setup import *

class Simson:
    def __init__(self):
        self.hr = 80
        self.skin = 1.2
        self.interest = 0.5

        self.k_hr = 1
        self.k_skin = 1
        self.k_interest = 1

    def react(self, feature):
        self.hr = self.k_hr*feature[0]
        self.skin = self.k_skin*feature[1]
        self.interest = self.k_interest*feature[2]

