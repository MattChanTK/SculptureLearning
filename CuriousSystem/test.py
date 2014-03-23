__author__ = 'Matthew'
from sklearn import svm

class store:
    def __init__(self):

        self.items = []

    def addItems(self, items):
        for item in items:
            self.items.append(item)

    def getItemsVal(self):
        vals = []
        for item in self.items:
            vals.append(item.val)
        return vals

class item:

    def __init__(self, val):
        self.val = val


def showItems():
    print 'storeA: ', storeA.getItemsVal()
    print 'storeB: ', storeB.getItemsVal()



svr = svm.SVR()




trainX = [[1,2,3,4], [3,4,5,6], [7,8,9,10]]
trainY = [10, 60, 80]
#svr.fit(trainX, trainY)
print svr.predict([1,2,3,9])
