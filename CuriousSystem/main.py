from setup import *
import Robot
import Simson
import Slider
import datetime
import random
import Q_learning
import Sensor
import threading
import Interface

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

# timing
clock = pygame.time.Clock()

# start animation flag
startFlag = False

#slider
sliderPos = 0
sliderPosInc = 0.0

feaHistory = []

# initialize sensor interface
class readSensorThread(threading.Thread):
    def __init__(self, com_port='COM8', baud_rate=9600):
        threading.Thread.__init__(self)
        self.running = False
        self.sx = Interface.Interface()
        self.comOpen = self.sx.initSensor(com_port=com_port, baud_rate=baud_rate)

    def run(self):
        self.running = True
        while self.running:
            self.sx.updateSensor()
        self.sx.closeSensor()

    def exitThread(self):
        self.running = False


    def pollSensor(self):
        return self.sx.getSensorState()

    def isRunning(self):
        return self.running

    def isComOpen(self):
        return self.comOpen

# start sensor thread
if simMode:
    pass
else:
    sxThread = readSensorThread(com_port=sensor_com_port, baud_rate=sensor_baud_rate)
    if sxThread.isComOpen():
        sxThread.start()
    else:
        print("Unable to communicate with sensors")
        print("Quitting program...")
        sxThread.exitThread()
        sys.exit()

while 1:

    clock.tick(fps)
    pygame.event.pump()

    # pygame interface update
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):

            # output to file
            if export_data:
                current_datetime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

                #prediction history
                file = open(os.path.join(output_folder, current_datetime + '_prediction_error'+'.csv'), 'a+') # append mode
                #for robot in pygame.sprite.Group.sprites(allRobots):  # for all robot
                for robot in robots[0:1]:  # for the first robot
                    numSample = len(robot.predict_history)
                    numDim = len(robot.predict_history[0])
                    for sample in robot.predict_history:
                        for dataPt in sample:
                            file.write(str(dataPt))
                            file.write(',')
                        file.write('\n')
                file.close()

                # action history
                file = open(os.path.join(output_folder, current_datetime + '_action_error'+'.csv'), 'a+') # append mode
                #for robot in pygame.sprite.Group.sprites(allRobots):  # for all robot
                for robot in robots[0:1]:  # for the first robot
                    numSample = len(robot.action_history)
                    numDim = len(robot.action_history[0])
                    for sample in robot.action_history:
                        for dataPt in sample:
                            file.write(str(dataPt))
                            file.write(',')
                        file.write('\n')
                file.close()

                fig = plt.figure(1)
                # subplotNum = len(3)*100 + 11
                # for type in range(3):
                #     plt.subplot(subplotNum)
                #     plt.plot(feaHistory[type])
                #     subplotNum += 1

                plt.plot(feaHistory)

               # plt.ylabel('Percent Action Taken (window='+str(window)+')')
                plt.xlabel('Time Step')
              #  plt.ylim([0, 1.0])
                plt.show()


            if not simMode:
                sxThread.exitThread()
            sys.exit()

        elif event.type == KEYDOWN and event.key == K_DOWN:
            sliderPosInc = -0.05
        elif event.type == KEYDOWN and event.key == K_UP:
            sliderPosInc = 0.05
        elif event.type == KEYUP:
            sliderPosInc = 0.0

    # sensor readings generation in simulation mode
    if simMode:

        num_robot_sim = 0
        hrFea = 0
        skinFea = 0
        interestFea = 0
        for robot in pygame.sprite.Group.sprites(allRobots):
            if -50 < robot.motor.accel < 50:
                print ("non-random")
                hrFea += robot.v
                skinFea += robot.v**2
                interestFea += robot.w*10
            else:
                print ("random")
                hrFea += abs(random.random()*5)
                skinFea += abs(random.random()*5)
                interestFea += abs(random.random()*5)

            num_robot_sim += 1


        fea = [sigmoid(0.1*(hrFea/num_robot_sim-10)),
               sigmoid(0.01*(skinFea/num_robot_sim-100)),
               sigmoid(2*(interestFea/num_robot_sim))]

        feaHistory.append(copy.copy([hrFea, skinFea, interestFea]))

        print("Simulated Sensor Readings")
        print("---- Heart Rate = " + str(fea[0]) + "  (" + str(hrFea/num_robot_sim) + ")" )
        print("---- Skin Conductance = " + str(fea[1]) + "  (" + str(skinFea/num_robot_sim) + ")")
        print("---- Interest Level = " + str(fea[2]) + " (" + str(interestFea/num_robot_sim) + ") ")


        # set user's response features
        user.setFea(fea)

        # calculate user engagement level
        Robot.Robot.updateEngage(fea)
        print("---- Level of Engagement = " + str(Robot.Robot.engage))

        # set start flag
        startFlag = True

    # real-time sensor input acquisition mode
    else:
        #get sensor readings
        sliderPos += sliderPosInc  # update slider position
        sxVal = sxThread.pollSensor()  # poll the sensor value from interface

        # robots move
        if sxVal is not None:

            fea = [sigmoid(0.005*(sxVal[0]-650)), sigmoid(0.02*(sxVal[1]-512)), sigmoid(sliderPos)]
            print("Sensor Readings")
            print("---- Heart Rate = " + str(fea[0]) + "  (" + str(sxVal[0]) + ")" )
            print("---- Skin Conductance = " + str(fea[1]) + "  (" + str(sxVal[1]) + ")")
            print("---- Interest Level = " + str(fea[2]))
            print("---- Level of Engagement = " + str(robots[0].engage))

            # set user's response features
            user.setFea(fea)
            feaHistory.append(copy.copy([sxVal[0], sxVal[1], sliderPos]))
            # calculate user engagement level
            Robot.Robot.updateEngage(fea)

            # set start flag
            startFlag = True

    if startFlag:
        # compute synchronous parameters
        if sync_behaviour:
            avgState = np.array([0.0, 0.0])
            num_robot_sync = 0
            for robot in pygame.sprite.Group.sprites(allRobots):
                 # use for updating the sync_state with average state
                 avgState += np.array(robot.getMotorParam())
                 num_robot_sync += 1
            avgState /= num_robot_sync

            #avgState = 0.01*random.random() - 0.005

            # update the synchronous state
            new_sync_state = np.array(Robot.Robot.getSyncState())
            #print("Sync Acceleration (init): " + str(new_sync_state))

            Robot.Robot.setSyncState(avgState.tolist())
        else:
            Robot.Robot.updateEngage(None)
        # update robot states
        allRobots.update(user)
        robot.memory.R.getNumExemplarRecursive()


    # draw robots on screen
    screen.blit(background, (0, 0))
    allRobots.draw(screen)


    pygame.display.flip()




'''
Might be useful later codes
---------------------------
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

'''

