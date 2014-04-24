from setup import *
import random
import Motor
import Sensor
import Memory
import Exemplar
import Q_learning


random.seed()

class Robot(pygame.sprite.Sprite):

    # synchronous state variables
    accel_sync = 0 #-0.1
    angAcc_sync = 0# -0.0005
    engage = 0.0  # level of engagement

    def __init__(self, this_robot_size=robot_size, simple=False):

        # pygame parameters
        # call Sprite intializer
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bluedot.jpg', -1)

        # resize the image
        self.image = pygame.transform.scale(self.image, robot_size)
        # resize the rect
        self.rect.size = this_robot_size

        # copy the screen
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        # state of the robot
        self.x = random.randint(self.area.left, self.area.right)
        self.y = self.area.bottom - random.randint(self.area.top, self.area.bottom)
        self.dir = random.random()*math.pi*2
        self.simple = simple

        # randomize the initial location of the dot
        self.rect.x = self.x
        self.rect.y = self.area.bottom - self.y

        # independent state variables
        # positiveV = random.randint(0, 1)
        # positiveW = random.randint(0, 1)
        self.v = 0 #10 * (positiveV + (1-positiveV)*-1)
        self.w = 0 #0.05 * (positiveW + (1-positiveW)*-1)
        # self.v = random.random()*20 - 10
        # self.w = random.random()*0.1 - 0.05
        self.motor = Motor.Motor(simple=self.simple)
        self.sensor = Sensor.Sensor(simple=self.simple)


        # instantiate the robot's memory
        self.memory = Memory.Memory()

        # Q-Learning engine
        self.Q = Q_learning.Q_learning(self.sensor, self.motor)

        # Prediction Error history
        self.predict_history = []

        # Action History
        self.action_history = []

        # State History
        self.state_history = []


    def update(self, user):

        # Sense the user
        self.__sense(user)
        s1 = copy.copy(self.sensor)

        # select action
        sm_q = self.__act()
        if self.isSimple():
            self.action_history.append(copy.copy(self.motor).getParam())
        else:
            self.action_history.append(Q_learning.Q_learning.discretize(copy.copy(self.motor), self.Q.m_state))
        m = copy.copy(self.motor)

        # predict results
        s2_predict = None
        if self.memory.getMemorySize() > 2:
            s2_predict, expert = self.__consult()

        # perform action
        self.__move()

        # check for actuation sensor inputs
        self.__sense(user)
        s2 = copy.copy(self.sensor)

        # Calculate prediction error
        lp = [0]*s2.getNumParam()
        if s2_predict is not None:
            lp = self.__observe(expert, s2_predict, s2)

        # Learn the consequence of the action
        self.__learn(sm_q, lp)

        self.memory.addExemplar(s1, m, s2)

        # self.printRegionPop()
        # print self.getSyncState()

    def __move(self):

        # calculate robot direction
        if self.isSimple():
            self.w = 0
        else:
            self.w += ((1-Robot.engage)*self.motor.getParam()[1] + Robot.engage*self.angAcc_sync)

        self.dir += self.w

        # computing the new position
        if self.isSimple():
            self.v += self.getSimpleMotor(self.motor)
            print("self.a: " + str(self.getSimpleMotor(self.motor)))
        else:
            self.v += ((1-Robot.engage)*self.motor.getParam()[0] + Robot.engage*self.accel_sync)
            print("self.a: " + str(self.motor.getVal()))

        print("self.v: " + str(self.v))
        print("self.w: " + str(self.w))

        dx = self.v*math.cos(self.dir)
        dy = self.v*math.sin(self.dir)
        #print "v  = " + str(self.v) + "    w = " + str(self.w) + "    dir = " + str(self.dir)
        # updating pygame rect position
        newpos = self.rect.move(dx, -dy)

        # check if it hits hall
        move_x = dx
        move_y = dy
        if not self.area.contains(newpos):
            # change direction if it does
            if newpos.left < self.area.left or newpos.right > self.area.right:
                move_x = -dx
            if newpos.top < self.area.top or newpos.bottom > self.area.bottom:
                move_y = -dy

            newpos = self.rect.move(move_x, -move_y)
        self.rect = newpos

        # remembering the state before to calculate velocity
        self.x0 = self.x
        self.y0 = self.y
        self.dir0 = self.dir

        # updating state
        self.x += move_x
        self.y += move_y

        # calculate new direction (will change if it hits wall)
        self.dir = math.atan2(move_y, move_x)

        # calculate new velocity
        self.v = math.sqrt((self.x-self.x0)**2 + (self.y-self.y0)**2)
        #self.w = self.dir-self.dir0

        # record state
        self.state_history.append((self.v, self.w))

    def __sense(self, user):
        self.sensor.setVal(user.getState())

    def __act(self):

        self.motor, sm_q = self.Q.getBestMotor(self.sensor)
        print("---- Motor State = "+ str(self.motor.getVal()))
        print("Best Q: " + str(sm_q))

        return sm_q

    def __consult(self):
        # consulting regional expert for action
        s2_predict, expert = self.memory.getPrediction(self.sensor, self.motor)
        #print s2_predict.getParam()
        return s2_predict, expert #reference to expert who made the prediction


    def __observe(self, expert, s2_predict, s2_actual):
        # compute error in prediction
        predict_error = expert.addPredictError(s2_actual, s2_predict)
       # print 'Prediction Error:', predict_error
        self.predict_history.append(predict_error)
        #print len(expert.error)
        # computer learning progress once sufficient sample is collected
        if len(expert.error) >= (expert.window + expert.smoothing):
            LP = expert.calcLearningProgress()
            #print LP
            return LP
        else:
            return [0]*self.motor.getNumParam()

    def __learn(self, q0, lp):

        alpha = Q_learning.Q_learning.learnRate
        gamma = Q_learning.Q_learning.gamma
        #q0 = self.Q.getQ(self.sensor, self.motor)
        reward = 0
        for comp in lp:
            reward += comp
        reward /= float(len(lp))

        q = q0 + alpha*(reward + gamma*(self.Q.getBestMotor(self.sensor))[1] - q0)

        self.Q.addQ(self.sensor, self.motor, q)

    def getState(self):
        return [self.v, self.w]

    def setState(self, new_x=None, new_y=None, new_dir=None):
        if new_x is not None:
            self.x = new_x

        if new_y is not None:
            self.y = new_y

        if new_dir is not None:
            self.dir = new_dir

        self.rect.x = self.x
        self.rect.y = self.y

    def getMotorParam(self):
        return self.motor.getParam()

    def printRegionPop(self):
        print len(self.memory.exp), '-->'
        self.memory.R.getNumExemplarRecursive()
        print('-----------')

    def getSyncState():
        return [Robot.accel_sync, Robot.angAcc_sync]
    getSyncState = staticmethod(getSyncState)

    def setSyncState(state):
        Robot.accel_sync = state[0]
        Robot.angAcc_sync = state[1]
    setSyncState = staticmethod(setSyncState)

    def updateEngage(sensorInputs):
        if sensorInputs is None:
            Robot.engage = 0
        else:
            Robot.engage = 0.20*sensorInputs[0] + 0.20*sensorInputs[1] + 0.60*sensorInputs[2]
    updateEngage = staticmethod(updateEngage)

    def getSimpleMotor(self, motor):
        if self.isSimple():
            states = Motor.Motor.getSimpleStates()
            if motor.getVal() == states[0]:
                output = -1
            elif motor.getVal() == states[1]:
                output = 1
            else:
                output = 0
        else:
            print("Motor not in simple mode!")
            raise
        return output

    def isSimple(self):
        return self.simple


