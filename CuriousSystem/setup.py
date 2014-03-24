import os
import sys
import pygame
import math
import datetime



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

def calcVariance(data):
    mean = sum(data)/len(data)
    sumDiff = 0
    for val in data:
        sumDiff += (val - mean)**2
    return sumDiff/(len(data))

def frange(x, y, jump):

    list = []
    while x < y:
        list.append(x)
        x += jump
    return list


num_robot = 1

bg_colour = (230, 240, 250)

fps = 30
sim_time = 10  # in second

size = (600, 400)
robot_size = (20, 20)

# Max number of exemplars before forgetting
memory_size = 5000

#Criterion
C1 = 250

# Expert Setting
time_window = 15
smoothing_parameter = 25

candy_up_size = (60, 60)
candy_down_size = (40, 40)
candy_factor_rate = 0.002



