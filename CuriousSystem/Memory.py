from setup import *
import Exemplar
import Region

class Memory:

    def __init__(self):

        # array to be used to store exemplars
        self.exp = []

        # the first region with nothing in it
        self.R = Region.Region()




    def addExemplar(self, s1, m, s2):
        # check if memory is full first
        if len(self.exp)+1 > memory_size:
            # forget oldest one if full
            forgotten = self.exp.pop(0)
            self.R.forgetExemplar(forgotten)

        newExemplar = Exemplar.Exemplar(s1, m, s2)
        self.exp.append(newExemplar)
        #print 'SM: ', newExemplar.getSM()
        splitted = self.R.addExemplar(self.exp[len(self.exp)-1])
        if splitted:
            self.R.getNumExemplarRecursive()

    def getPrediction(self, sensor, motor):
        expert = self.R.getExpert(sensor, motor)
        return expert.predict(sensor, motor), expert

    def getMemorySize(self):
        return len(self.exp)

