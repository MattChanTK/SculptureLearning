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
    for robot in pygame.sprite.Group.sprites(allRobots):

        if Q_learning.Q_learning.discretize(robot.motor)[0] < 1 & Q_learning.Q_learning.discretize(robot.motor)[1] < 1:

            hrFea = 0.5 #100
            # distance to centre
            skinFea = 0.5 #2.5
            # average angular velocity
            interestFea = 0.5
            '''
            # just average speed for now
            hrFea = abs(robot.motor.v)
            # distance to centre
            skinFea = abs(robot.motor.v)/1.2
            # average angular velocity
            interestFea = abs(robot.motor.v)/50#abs(robot.motor.w/(math.pi/4.0))


        elif Q_learning.Q_learning.discretize(robot.motor)[0] < 0:
             # just average speed for now
            hrFea = abs(math.sin(robot.motor.v))*50.0
            # distance to centre
            skinFea = abs(math.cos(robot.motor.v))*50.0
            # average angular velocity
            interestFea = abs(math.log(abs(robot.motor.w)+0.001)/math.log(abs(math.pi/4.0))+0.001)
            '''
        else:
            '''
            bounds = Sensor.Sensor.getBound()
            hrFea = random.uniform(bounds[0][0], bounds[0][1])#/(user.hr+0.001)
            skinFea = random.uniform(bounds[1][0], bounds[1][1])#/(user.k_skin+0.001)
            interestFea = random.uniform(bounds[2][0], bounds[2][1])#/(user.k_interest+0.0001)
            '''
             # just average speed for now
            hrFea = abs(robot.v)
            # distance to centre
            skinFea = abs(robot.v)**2
            # average angular velocity
            interestFea = abs(robot.v)**2#abs(robot.motor.w/(math.pi/4.0))



        num_robot += 1
        #print robot.memory.R.getNumRegion()
    fea = [hrFea/num_robot, skinFea/num_robot, interestFea/num_robot]

    user.react(fea)


    screen.blit(background, (0, 0))
    allRobots.draw(screen)

    pygame.display.flip()


