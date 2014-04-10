from setup import *
import Robot
import Simson
import Slider
import datetime
import random
import Q_learning
import Sensor

# pygame set up
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Experiment Interface')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(bg_colour)

# instantiate robots
robots = []
for i in range(0, num_robot):
    robot = Robot.Robot()
    robots.append(robot)

# instantiate user
user = Simson.Simson()

# add elements to pygame space
allRobots = pygame.sprite.Group()

for i in range(0, num_robot):
    allRobots.add(robots[i])

#timing
clock = pygame.time.Clock()

while 1:

    clock.tick(fps)

    # pygame update
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):

            # output to file
            current_datetime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

            #prediction history
            file = open(os.path.join('outputs', current_datetime + '_prediction_error'+'.csv'), 'a+') # append mode
            for robot in pygame.sprite.Group.sprites(allRobots):
                numSample = len(robot.predict_history)
                numDim = len(robot.predict_history[0])
                for sample in robot.predict_history:
                    for dataPt in sample:
                        file.write(str(dataPt))
                        file.write(',')
                    file.write('\n')
            file.close()

            # action history
            file = open(os.path.join('outputs', current_datetime + '_action_error'+'.csv'), 'a+') # append mode
            for robot in pygame.sprite.Group.sprites(allRobots):
                numSample = len(robot.action_history)
                numDim = len(robot.action_history[0])
                for sample in robot.action_history:
                    for dataPt in sample:
                        file.write(str(dataPt))
                        file.write(',')
                    file.write('\n')
            file.close()
            sys.exit()


    # robots move
    allRobots.update(user)

    # user reacts to the animation
    num_robot = 0
    hrFea = 0.0
    skinFea = 0.0
    interestFea = 0.0
    avgState = np.array([0.0, 0.0])

    for robot in pygame.sprite.Group.sprites(allRobots):

        if Q_learning.Q_learning.discretize(robot.motor)[0] < 1 & Q_learning.Q_learning.discretize(robot.motor)[1] < 1:

            hrFea += 0.5
            # distance to centre
            skinFea += 0.5
            # average angular velocity
            interestFea += 0.5


        elif Q_learning.Q_learning.discretize(robot.motor)[0] < 4 & Q_learning.Q_learning.discretize(robot.motor)[1]<4:
             # just average speed for now
            hrFea += abs(robot.v)
            # distance to centre
            skinFea += abs(robot.v)**2
            # average angular velocity
            interestFea += abs(robot.v)**2

        else:

            bounds = Sensor.Sensor.getBound()
            hrFea += random.uniform(bounds[0][0], bounds[0][1])#/(user.hr+0.001)
            skinFea += random.uniform(bounds[1][0], bounds[1][1])#/(user.k_skin+0.001)
            interestFea += random.uniform(bounds[2][0], bounds[2][1])#/(user.k_interest+0.0001)

        avgState += np.array(robot.getState())
        num_robot += 1

        #print robot.memory.R.getNumRegion()
    avgState /= num_robot
    fea = [hrFea/num_robot, skinFea/num_robot, interestFea/num_robot]
    user.react(fea)

    # update the synchronous state

    for robot in pygame.sprite.Group.sprites(allRobots):
        robot.setSyncState(avgState.tolist())


    screen.blit(background, (0, 0))
    allRobots.draw(screen)

    pygame.display.flip()


