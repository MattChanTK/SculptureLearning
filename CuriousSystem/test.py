__author__ = 'Matthew'

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

storeA = store()
storeB = store()

storeA.addItems([item(1), item(2), item(3)])

showItems()

storeB.addItems(storeA.items)

showItems()

storeA.items[1] = item(23)
showItems()

storeB.items.remove(storeA.items[1])
showItems()

