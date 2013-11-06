from globalVar import*
import numpy as np
import math


# a single pressure mat (switch based)
class Mat():

    sensor = np.zeros((math.floor(roomSizeY/matSizeY), math.floor(roomSizeX/matSizeX)),dtype=bool)
   
   # def __init__(self):

         
