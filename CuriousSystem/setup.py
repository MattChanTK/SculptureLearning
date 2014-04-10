import os
import sys
import pygame
import math
import datetime
import copy
import numpy as np
import time



from pygame.locals import *
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

def load_image(name, colorkey=None):
    fullname = os.path.join('img', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    #image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('audio', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', name
        raise SystemExit, message
    return sound

def calcVariance(dataRaw):
    # calcVarStart = time.clock()

    data = np.array(dataRaw, dtype=float)
    cardinalS, dimS = data.shape
    mean = np.mean(data, axis=0)
    diff = [0]*cardinalS

    for i in range(0, cardinalS):
        diff[i] = np.linalg.norm((data[i, :] - mean), 1)**2 # find difference from mean
   # print "   --> inside calc var: " + str(time.clock()-calcVarStart)
    return sum(diff)/cardinalS

def frange(x, y, div):

    list = []
    jump = (y - x)/float(div)
    for i in range(0, div):
        list.append(x + i*jump)
    return list

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

num_robot = 4

bg_colour = (230, 240, 250)

fps = 30
sim_time = 10  # in second

size = (900, 600)
robot_size = (20, 20)

# Max number of exemplars before forgetting
memory_size = 5000

#Criterion
C1 = 250

# Expert Setting
time_window = 3
smoothing_parameter = 5



