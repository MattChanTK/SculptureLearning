from setup import *
class Exemplar:

    def __init__(self, s, m, s2):
        self.S = s
        self.M = m
        self.S2 = s2


    def getNumParams(self):
        return self.S.getNumParam() + self.M.getNumParam() + self.S2.getNumParam()

    def getNumOutputParams(self):
        return self.S2.getNumParam(), self.S.getNumParam() + self.M.getNumParam()

    def getVal(self, dim=-1):

        vals = self.S.getParam() + self.M.getParam() + self.S2.getParam()
        if dim == -1:
            return vals
        return vals[dim]

    def getSM(self):

        return self.S.getParam() + self.M.getParam()

    def getS2(self):

        return self.S2.getParam()

