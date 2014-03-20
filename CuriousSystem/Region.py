from setup import *
import Motor
import Sensor


class Region:
    def __init__(self, exemplars=None):
        self.left = None
        self.right = None
        if exemplars is None:
            self.exemplars = []
        else:
            self.exemplars = exemplars

    def getLeftChild(self):
        return self.left

    def getRightChild(self):
        return self.right

    def updateRegions(self):
        # need codes for forgetting exemplar
        # it's leaf node
        if self.left is None and self.right is None:
            # split if C1 is met
            if self.getNumExemplar() > C1:
                self.split()
        elif self.left is not None and self.right is not None:
            self.left.updateRegions()
            self.right.updateRegions()
        else:
            # there's no right node, only left node
            if self.right is None:
                #this node absorbs the right node
                temp = self.left
                self.right = self.left.right
                self.left = self.left.left
                del(temp)

            # there's no left node, only right node
            elif self.left is None:
                #this node absorbs the left node
                temp = self.right
                self.left = self.right.left
                self.right = self.right.right
                del(temp)

            self.updateRegions()


    def addExemplar(self, exemplar):
        self.updateRegions()
        # adding an exemplar
        self.exemplars.append(exemplar)

        #check where it should add the exemplar to
        if self.left is None and self.right is None:
            # leave the exemplar here
            pass
        else:
            # determining to add the exemplar to left or right node

            # check context
            leftContext = self.left.getContext()
            rightContext = self.right.getContext()

            # if the context is more similar to the left node than right node
            if abs(exemplar.S.hr - leftContext[0]) < abs(exemplar.S.hr - rightContext[0]):
                self.left.addExemplar(exemplar)
            else:
                self.right.addExemplar(exemplar)

    def getExemplar(self):
        return self.exemplars

    def getNumExemplar(self):
        return len(self.exemplars)

    def split(self):

        numExemplar = self.getNumExemplar()
        self.left = Region(self.exemplars[0:numExemplar/2])
        self.right = Region(self.exemplars[numExemplar/2:numExemplar])

    def getNumRegion(self):

        if self.getLeftChild() is None:
            return 1
        else:
            return self.getLeftChild().getNumRegion() + self.getRightChild().getNumRegion()

    def getContext(self):

        numSParam = self.exemplars[0].S.getNumParam()
        numMParam = self.exemplars[0].M.getNumParam()
        numS2Param = self.exemplars[0].S2.getNumParam()

        avg = [0]*(numSParam + numMParam + numS2Param)
        for exp in self.exemplars:

            # Sensor parameters
            for i in range(0, numSParam):
                avg[i] += exp.S.getParam()[i]
            # Motor parameters
            for i in range(numSParam, numSParam + numMParam):
                avg[i] += exp.M.getParam()[i - numSParam]
            # Sensor(t+1) parameters
            for i in range(numSParam + numMParam, numSParam + numMParam + numS2Param):
                avg[i] += exp.S2.getParam()[i - numSParam - numMParam]

        # divide by total number of exemplar one by one
        numExp = self.getNumExemplar()
        for i in range(0, len(avg)):
            avg[i] /= numExp

        return avg