class Exemplar:

    def __init__(self, s, m, s2):
        self.S = s
        self.M = m
        self.S2 = s2

    def getNumParams(self):
        return self.S.getNumParam() + self.M.getNumParam() + self.S2.getNumParam()

    def getNumOutputParams(self):
        return self.S2.getNumParam()

    def getVal(self, dim):

        vals = self.S.getParam()
        vals.append(self.M.getParam())
        vals.append(self.S2.getParam())
        return vals[dim]


