from setup import *

class Simson:
    def __init__(self):
        self.hr = 80
        self.skin = 1.2
        self.interest = 0.5

        self.k_hr = 8
        self.k_skin = 0.01
        self.k_interest = 0.1

    def react(self, feature):
        self.hr = self.k_hr*feature[0]
        self.skin = self.k_skin*feature[1]
        self.interest = self.k_interest*feature[2]