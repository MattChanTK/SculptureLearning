import os
import sys
import pygame
import math
import datetime
import copy
import numpy as np
import time
import matplotlib.pyplot as plt



from pygame.locals import *
if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

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
        diff[i] = np.linalg.norm((data[i, :] - mean)/mean, 1)**2 # find difference from mean
   # print "   --> inside calc var: " + str(time.clock()-calcVarStart)
    return sum(diff)/cardinalS

def frange(x, y, div):

    list = []
    jump = (y - x)/float(div)
    for i in range(0, div):
        list.append(x + i*jump)
    return tuple(list)

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

#prediction history
def exportToCSV(current_datetime, filename, robot_history):
    with open(os.path.join(output_folder, current_datetime + '_' + filename+'.csv'), 'a+') as file: # append mode

        for sample in robot_history:
            for dataPt in sample:
                file.write(str(dataPt))
                file.write(',')
            file.write('\n')
    file.close()

# number of blue dots
num_robot = 1

# sync behaviours
sync_behaviour = False

# number of updates per second
fps = 40

# ==== simulation mode setting ====
# simulation mode on or off
simMode = True
simpleMode = True
num_simpleStates_s = 100
num_simpleStates_m = 3

# can't turn on simple mode unless in simulation
if simMode == False:
    simpleMode = False


# ==== sensor interface setting ====
sensor_com_port = 'COM8'
sensor_baud_rate = 9600

# ==== graphical interface settings ====
bg_colour = (230, 240, 250)
size = (900, 600)
robot_size = (20, 20)

# ===== Learning algorithm settings =====
# Max number of exemplars before forgetting
memory_size = 50000

# Criterion 1
C1 = 250

# Expert Setting
time_window = 3
smoothing_parameter = 5

# ==== Q-learning setting ====
num_s_division = 10  # discretization
num_m_division = 3


# ==== data collection settings
output_folder = 'outputs'
export_data = True
show_plot = True
printToTerm = False
