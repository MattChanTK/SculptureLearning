from setup import *
import random
import Expert

class Region:
    def __init__(self, j0=None, vj0=None, exemplars=None):
        self.left = None
        self.right = None
        self.expert = Expert.Expert()

        if exemplars is None:
            self.exemplars = []
        else:
            self.exemplars = exemplars
            self.expert.train(self.exemplars)

        self.cut_dim = None
        self.cut_val = None

        self.cut_dim_0 = j0
        self.cut_val_0 = vj0



    def getLeftChild(self):
        return self.left

    def getRightChild(self):
        return self.right

    def updateRegions(self):
        splitted = False
        # Forgetting region that has no exemplar
        if self.left is not None and self.left.getNumExemplar() == 0:
            self.left = None
        elif self.right is not None and self.right.getNumExemplar() == 0:
            self.right = None

        # it's leaf node
        if self.left is None and self.right is None:
            # split if C1 is met
            if self.getNumExemplar() > C1:
                splitted = self.split()
        elif self.left is not None and self.right is not None:

            splitted |= self.left.updateRegions()
            splitted |= self.right.updateRegions()
        else:
            # there's no right node, only left node
            if self.right is None:
                #this node absorbs the right node
                self.expert = self.left.expert
                self.cut_dim = self.left.cut_dim
                self.cut_val = self.left.cut_val
                self.right = self.left.right
                self.left = self.left.left

            # there's no left node, only right node
            elif self.left is None:
                #this node absorbs the left node
                self.expert = self.right.expert
                self.cut_dim = self.right.cut_dim
                self.cut_val = self.right.cut_val
                self.left = self.right.left
                self.right = self.right.right

            splitted |= self.updateRegions()

        return splitted

    def addExemplar(self, exemplar):
        splitted = False
        splitted |= self.updateRegions()
        # adding an exemplar
        self.exemplars.append(exemplar)

        #check where it should add the exemplar to
        if self.left is None and self.right is None:
            # leave the exemplar here
            # training expert
            if len(self.exemplars) > 1:
                self.expert.train(self.exemplars)
        else:
            # determining to add the exemplar to left or right node
            if exemplar.getVal(self.cut_dim) < self.cut_val:
                splitted |= self.left.addExemplar(exemplar)
            elif exemplar.getVal(self.cut_dim) > self.cut_val:
                splitted |= self.right.addExemplar(exemplar)
            else:
                if self.left.getNumExemplar() > self.right.getNumExemplar():
                    splitted |= self.right.addExemplar(exemplar)
                else:
                    splitted |= self.left.addExemplar(exemplar)
        return splitted

    def forgetExemplar(self, exemplar):
        #self = self.updateRegions()
        try:
            self.exemplars.remove(exemplar)

            # delete from the child branches
            if self.left is not None:
                self.left.forgetExemplar(exemplar)
            if self.right is not None:
                self.right.forgetExemplar(exemplar)

            #if self.right is None and self.right is None:
            #    print 'exemplar deleted'

        except ValueError:
            # don't need to search this branch
            pass

    def getExemplar(self):
        return self.exemplars

    def getNumExemplar(self):
        return len(self.exemplars)

    def getNumExemplarRecursive(self, level=0):

        numInLeft = 0
        numInRight = 0
        if self.left is not None:
            numInLeft = self.left.getNumExemplarRecursive(level+1)

        if self.right is not None:
            numInRight = self.right.getNumExemplarRecursive(level+1)

        if self.right is None and self.left is None:
            print('\t'*level),
            print(str(len(self.exemplars)))

            return len(self.exemplars)

        print('\t'*level),
        print(numInLeft + numInRight),
        print(' [' + str(self.cut_dim) + ', ' + str(self.cut_val) + ']')
        return numInLeft + numInRight

    def split(self):

        # estimate the best Criterion 2
        c2 = self.getBestC2()
        j = c2[0]
        vj = c2[1]

        if j < 0:
            print ('ERROR: j cannot be less than 0!')

        if j == self.cut_dim_0 and vj == self.cut_val_0:
            return False
        r1, r2 = self.applyC2(j)

        # instantiate the new sub regions
        self.left = Region(exemplars=r1, j0=j, vj0=vj)
        self.right = Region(exemplars=r2, j0=j, vj0=vj)
        print ('Split Region')


        # record the new j and vj
        self.cut_dim = j
        self.cut_val = vj

        return True


    def applyC2(self, j):

        sortedExp = sorted(self.exemplars, key=lambda exp: exp.getVal(j))
        r1 = sortedExp[0:int(len(sortedExp)/2)]
        r2 = sortedExp[int(len(sortedExp)/2):int(len(sortedExp))]

        return r1, r2

    def getExpValArray(expSet, dim=-1):
        data = []
        for exp in expSet:
            data.append(exp.getVal(dim)) # all the val in i-th dimension
        return data
    getExpValArray = staticmethod(getExpValArray)

    def getBestC2(self):
        #start = time.clock()
        #print "Start Time: " + str(start)
        # getting the number of dimension in SM
        numDim = len(self.exemplars[0].getSM())
        SM_index = 0
        #numDim, S2_index = self.exemplars[0].getNumOutputParams()

        # keeping tracking of the best C2
        bestC2 = [-1, -1, -1] #[j, vj, var]

        # for each dimension
        for j in range(SM_index, SM_index + numDim):

            #dimStart = time.clock()

            # split set equally, sorted
            #applyC2Start = time.clock()
            set1, set2 = self.applyC2(j)
            vj = (set1[-1].getVal(j) + set2[0].getVal(j))/2.0

            # print "         # Set1: " +  str(len(set1)) + "    # Set2: " + str(len(set2))
            #print "     Apply C2(" +str(j) +","+str(vj)+"" "): " + str(time.clock()-applyC2Start)

            # calculate the sum of (sum of dimensional variances) in each set
            if not set1 or not set2: # if of the set is empty
                pass
            else:
                #calcVarStart = time.clock()
                set1Array = Region.getExpValArray(set1)
                set2Array = Region.getExpValArray(set2)

                var1 = calcVariance(set1Array)
                var2 = calcVariance(set2Array)

                # sum of total variance
                var = var1 + var2

                # update best C2 is better than current best
                if bestC2[2] < 0 or bestC2[2] < var:
                    bestC2[2] = var
                    bestC2[1] = vj
                    bestC2[0] = j
              #  print "     Calc Var(" +str(j) +","+str(vj)+"" "): " + str(time.clock()-calcVarStart)

           # print "   dimension Loop(" +str(j) + "): " + str(time.clock() - dimStart)
       # print "  -->Duration: " + str(time.clock()-start)
        return bestC2

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

 #   def calcLearnRate(self):

    def getExpert(self, sensor, motor):
        sm = sensor.getParam() + motor.getParam()

        if self.left == None and self.right == None:
            return self.expert
        else:
             # determining to look for expert in the left or right node
            if sm[self.cut_dim] < self.cut_val:
                return self.left.getExpert(sensor, motor)
            else:
                return self.right.getExpert(sensor, motor)





