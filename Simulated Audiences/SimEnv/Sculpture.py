from globalVar import*

import Attractor


class Sculpture:

    def __init__(self):
        #number of attractor
        self.numAtt = 4
        # size of sculpture
        self.artSizeX = 100
        self.artSizeY = 100
        self.artSize = [self.artSizeX, self.artSizeY]

        # centre location
        self.artLowerLeft = [100, 50]

        # Creating the sculptures
        self.att = [Attractor.Attractor() for i in range(self.numAtt)]

        for i in range(self.numAtt):
            self.att[i].randomInit(self.artLowerLeft, self.artSize)

