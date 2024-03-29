__author__ = 'Matthew'
from sklearn import svm
import copy

class store:
    def __init__(self):

        self.items = []
        self.a = 0
        self.b = 0

    def __repr__(self):

        return repr((self.a, self.b))

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


storeA = store()
storeB = store()
storeA.a = 10
storeA.b = 100

stores = [storeA, storeB]
print stores
sortedStores = sorted(stores, key=lambda store: store.a)
print sortedStores


arr = [1,2]
for x in arr[0:1]:
    print x
'''

svr = svm.SVR()


storeA = [1.0,2.0,item(5),4]
storeB = storeA
print storeA
print storeB
storeB[1] = storeB[1]/10
print storeA
print storeB[2].val

'''
'''
trainX = [[1,2,3,4], [3,4,5,6], [7,8,9,10]]
trainY = [10, 60, 80]
svr.fit(trainX, trainY)
predict = svr.predict([[1,2,3,9], [7,8,9,10]])
print predict

set = []
for i in range(3):
    set.append([0]*2)

print set
set [0][0] = 2
print set

set2 = copy.copy(set)
set2.append([12]*len(set[0]))
print set
print set2
'''