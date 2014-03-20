from setup import *


class Motor():

    def __init__(self):
        self.v = 0  # velocity
        self.w = 0  # angular velocity

    def getParam(self):
        return [self.v, self.w]

    def getNumParam(self):
        return len(self.getParam())
