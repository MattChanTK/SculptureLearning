from globalVar import*
import random

class Attractor:


    def __init__(self):

        # location
        self.x = 0
        self.y = 0

        # State
        self.attOn = False
        self.attLevel = 1

    def randomInit(self, artLowerLeft, artSize):
        self.x = artLowerLeft[0] + random.random()*artSize[0]
        self.y = artLowerLeft[1] + random.random()*artSize[1]

        self.attOn = True
        self.attLevel = random.randint(1, 3)



    def set(self, x, y, attOn, attLevel):

        #set initial condition
        self.x = x
        self.y = y
        self.attOn = attOn
        self.attLevel = attLevel







