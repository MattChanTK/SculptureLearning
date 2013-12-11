from globalVar import*

import random

import math

random.seed()

# Simulated Person
class SimSon:

    minV = 0
    maxV = 100
    minOmega = -math.pi/10
    maxOmega = math.pi/10

    angShiftStdDev = 0.008

    def __init__(self):

        #set state
        self.x = 0
        self.y = 0
        self.r = 0

        #field of view
        self.fov = math.radians(150)

        #personal interest in art
        self.interest = 0.5  #max 1; min 0
        self.angShiftStdDev = 0.008

        #distance reduction vs speed constants
        self.speedReduceK = 0.02

        #set initial speed
        self.v = random.uniform(SimSon.minV, SimSon.maxV)
        self.omega = random.uniform(SimSon.minOmega, SimSon.maxOmega)


        #enter room
        self.enterRoom()
        
    def enterRoom(self):


        #decide to come in on left/right or top/bottom
        leftRight = random.randint(0,1)

        #generate random state
        if (leftRight):
            #random location
            self.y = random.random()*roomSizeY

            if (random.randint(0, 1)):
                #coming from the right
                self.x = roomSizeX
                rMid = math.pi
            else:
                #coming from the left
                self.x = 0
                rMid = 0
        else:
            #random location
            self.x = random.random()*roomSizeX

            if (random.randint(0, 1)):
                #coming from the top
                self.y = 0
                rMid = math.pi/2
            else:
                #coming from the bottom
                self.y = roomSizeY
                rMid = 3/2*math.pi

        self.r = random.uniform(rMid - math.pi/3, rMid +math.pi/3)
    def update(self):
        #update state of the person
        self.x = self.x + max(0,self.v)*math.cos(self.r)/frameRate + 0.1*random.gauss(0, 1)
        self.y = self.y + max(0,self.v)*math.sin(self.r)/frameRate + 0.1*random.gauss(0, 1)
     #   self.r = (self.r + self.omega/frameRate + 0.01*random.gauss(0, 1) + 2*math.pi) % (2*math.pi)

        if random.random()<0.01:
            self.v = self.v + random.gauss(0 , 1)
            if self.v < SimSon.minV:
                self.v = SimSon.minV
            elif self.v> SimSon.maxV:
                self.v = SimSon.maxV
                
        if random.random()<0.01:
            self.omega = self.omega + random.gauss(0,1)
            if self.omega < SimSon.minOmega:
                self.omega = SimSon.minOmega
            elif self.omega> SimSon.maxOmega:
                self.omega = SimSon.maxOmega
        

        #reinitialize person if leaving room
        if ((self.x < 0) | (self.x > roomSizeX) | (self.y < 0) | (self.y > roomSizeY)):
            #print('person reentered')
            #print ("(%f,%f, %f)" %(self.x, self.y, math.degrees(self.r)))
            #print ("v = %f   omega = %f" %(self.v, math.degrees(self.omega)))
            self.__init__();
    def attIsInFOV(self, art):

        angleToAtt = [0] * art.numAtt
        #get the angle of the attractor relative to the person
        for i in range(art.numAtt):
            angleToAtt[i] = math.atan2(art.att[i].y - self.y, art.att[i].x - self.x)

        distToAtt = [0] * art.numAtt
        #get the distance of the attractor relative to the person
        for i in range(art.numAtt):
            distToAtt[i] = math.sqrt((art.att[i].x - self.x)**2 + (art.att[i].y - self.y)**2)

        attInFov = [0] * art.numAtt

        for i in range(art.numAtt):
            if (self.r + self.fov/2) > 2*math.pi:
                angleToAtt[i] = angleToAtt[i] + 2*math.pi

            attInFov[i] = (angleToAtt[i] < (self.r + self.fov/2)) & \
                            (angleToAtt[i] > (self.r - self.fov/2))

        return [attInFov, angleToAtt, distToAtt]

    def angleShift(self, art, attInFOV):
        #[attInFov, angleToAtt] = self.attIsInFOV(art)
        attInFov = attInFOV[0]
        angleToAtt = attInFOV[1]

        sumOfAttLevel = 0
        angShift = 0
        for i in range(len(attInFov)):
            # if the attractor is in FOV
            if art.att[i].attOn & attInFov[i]:
                angShift += art.att[i].attLevel*(angleToAtt[i] - self.r)
                sumOfAttLevel += art.att[i].attLevel


        if sumOfAttLevel > 0:
            angShift /= sumOfAttLevel

        return angShift
    def speedReduce(self, art, attInFOV):
        attInFov = attInFOV[0]
        distToAtt = attInFOV[2]

        sumOfAttLevel = 0
        speedReduce = 0
        for i in range(len(attInFov)):
             # if the attractor is in FOV
            if art.att[i].attOn & attInFov[i]:
                speedReduce += art.att[i].attLevel*(distToAtt[i])
                sumOfAttLevel += art.att[i].attLevel

        if sumOfAttLevel > 0:
            speedReduce /= sumOfAttLevel

        return speedReduce

    def lookToAttractor(self, art):
        attInFov = self.attIsInFOV(art)

        meanAngShift = self.angleShift(art, attInFov)
        newR = random.gauss(self.r + self.interest*meanAngShift, SimSon.angShiftStdDev)
        self.r = (newR + 2*math.pi) % (2*math.pi)

        meanSpeedReduce = self.speedReduce(art, attInFov)
        self.v = max(SimSon.minV, self.v*self.speedReduceK*meanSpeedReduce)
        #print(self.v)















