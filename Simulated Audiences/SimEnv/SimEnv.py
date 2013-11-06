# Numpy is a library for handling arrays (like data points)
import numpy as np

# Pyplot is a module within the matplotlib library for plotting
from matplotlib import pyplot as plt
from matplotlib import animation

import math

from globalVar import*
import SimSon
import Attractor
import Sculpture


# Creating people
person = [SimSon.SimSon() for i in range(numSimSon)]

for i in range(numSimSon):
    print("(%f,%f, %f)" %(person[i].x, person[i].y, math.degrees(person[i].r)))
    #plt.plot(person[i].x, person[i].y,'ro')


# Creating the sculptures
art = Sculpture.Sculpture()


# Running
if drawingOn:
    plt.ion()


    for frame in range(numFrame):
        # clear plot

        plt.clf()

        #plot the boundary of the sculpture
        plt.plot([art.artLowerLeft[0], art.artLowerLeft[0]],
                 [art.artLowerLeft[1], art.artLowerLeft[1]+art.artSizeY], 'k-.', lw=1)
        plt.plot([art.artLowerLeft[0]+art.artSizeX, art.artLowerLeft[0]+art.artSizeX],
                 [art.artLowerLeft[1], art.artLowerLeft[1]+art.artSizeY], 'k-.', lw=1)
        plt.plot([art.artLowerLeft[0], art.artLowerLeft[0]+art.artSizeX],
                 [art.artLowerLeft[1], art.artLowerLeft[1]], 'k-.', lw=1)
        plt.plot([art.artLowerLeft[0], art.artLowerLeft[0]+art.artSizeX],
                 [art.artLowerLeft[1]+art.artSizeY, art.artLowerLeft[1]+art.artSizeY], 'k-.', lw=1)

        #plot the attractor location
        for i in range(art.numAtt):
            plt.plot(art.att[i].x, art.att[i].y, 'bx')


        print ("Frame %d" %frame)
        for i in range(numSimSon):

            person[i].lookToAttractor(art)
            person[i].update()

            #plot the person location
            plt.plot(person[i].x, person[i].y,'ro')
            #plot the direction indicator
            plt.plot([person[i].x, person[i].x+(5*math.cos(person[i].r))],
                     [person[i].y, person[i].y+(5*math.sin(person[i].r))], 'b-')
            #print ("(%f,%f, %f)" %(person[i].x, person[i].y, math.degrees(person[i].r)))
            #print ("v = %f   omega = %f" %(person[i].v, math.degrees(person[i].omega)))

        plt.axis([0, roomSizeX, 0, roomSizeY])
        plt.draw()

    plt.ioff()
    plt.show()



'''
# set up figure and animation
fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(0, roomSizeX), ylim=(0, roomSizeY))

# holds the locations of the SimSon's location
people = ax.plot([],[],'bo', ms = 6)


def init():
    """initialize animation"""
    peopleX = []
    peopleY = []
    return peopleX, peopleY

def animate(i):
    """perform animation step"""
    global frameRate, ax, fig
    for i in range(numSimSon):
        person[i].update()
        peopleX.append(person[i].x)
        peopleY.append(person[i].y)
 

##    ms = int(fig.dpi * 2 * box.size * fig.get_figwidth()
##             / np.diff(ax.get_xbound())[0])
    
    # update pieces of the animation
   # rect.set_edgecolor('k')
    #people.set_data(box.state[:, 0], box.state[:, 1])
    people.set_markersize(ms)
    return peopleX, peopleY

ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=10, blit=True, init_func=init)
plt.show()
'''
