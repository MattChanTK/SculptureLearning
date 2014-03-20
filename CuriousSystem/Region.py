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

    def addExemplar(self, exemplar):
        self.exemplars.append(exemplar)

        if self.left is not None:
            leftContext = self.left.getContext()

        #if exemplar.S

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

        avg = [0]*(numSParam + numMParam)
        for exp in self.exemplars:

            # Sensor parameters
            for i in range(0, numSParam):
                avg[i] += exp.S.getParam()[i]
            # Motor parameters
            for i in range(numSParam, numMParam):
                avg[i] += exp.M.getParam()[i - numSParam]

        # divide by total number of exemplar one by one
        numExp = self.getNumExemplar()
        for i in range(0, len(avg)):
            avg[i] /= numExp

        return avg