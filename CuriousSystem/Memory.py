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
        if len(self.exp)+1 > mem_size:
            # forget oldest one if full
            forgotten = self.exp.pop(0)
            self.R.forgetExemplar(forgotten)

        newExemplar = Exemplar.Exemplar(s1, m, s2)
        self.exp.append(newExemplar)

        self.R.addExemplar(self.exp[len(self.exp)-1])




    #def forgetExemplar(self):


