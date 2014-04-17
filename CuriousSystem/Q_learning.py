from setup import*
import Sensor
import Motor
import random


class Q_learning():

    division = 10  # number of sensor states per dimension
    greed = 0.35
    learnRate = 0.2
    gamma = 1.0

    # mapping sensor values into discrete set of states
    s_state = []
    bounds = Sensor.Sensor.getBound()
    for i in range(0, len(bounds)):
        discrete_states = frange(bounds[i][0], bounds[i][1], division)
        s_state.append(discrete_states)
        print("Sensor States[" + str(i) + "]: " + str(discrete_states))
    # mapping motor values into discrete set of states
    m_state = []
    bounds = Motor.Motor.getBound()
    for i in range(0, len(bounds)):
        discrete_states = frange(bounds[i][0], bounds[i][1], division)
        m_state.append(discrete_states)
        print("Motor States[" + str(i) + "]: " + str(discrete_states))

    def __init__(self):

        # Q value (weight for each action)
        self.q_table = dict()

    def discretize(input):
        # sensor/motor state per dimension
        s = [0]*input.getNumParam()

        # check if it's a sensor input or motor input
        if type(input) is Sensor.Sensor:
            state = Q_learning.s_state
        else:
            state = Q_learning.m_state

        # mapping value into discrete set of states
        for i in range(0, len(s)):
            s_raw = input.getParam()[i]
            for label in range(0, len(state[i])):
                if s_raw < state[i][label]:
                    s[i] = label
                    break
                elif s_raw > state[i][len(state[i])-1]:
                    s[i] = len(state[i])-1
        return tuple(s)
    discretize = staticmethod(discretize)

    def __getMotor(self, input):

        motorVal = []
        for i in range(0, len(input)):
            motorVal.append(Q_learning.m_state[i][input[i]])
        return Motor.Motor(motorVal)

    def getQ(self, sensor, motor):
        s = Q_learning.discretize(sensor)

        if type(motor) is Motor.Motor:
            m = Q_learning.discretize(motor)
        else:
            m = motor

        if s + m in self.q_table:
            return self.q_table[s + m]
        else:
            return 0

    def addQ(self, sensor, motor, q_val):
        s = Q_learning.discretize(sensor)
        m = Q_learning.discretize(motor)

        self.q_table[s+m] = q_val

    def getBestMotor(self, sensor):

        # at random choose an random action
        k = random.random()
        if k < Q_learning.greed:
            motor = Q_learning.getRandomMotor()
            return motor, self.getQ(sensor, motor)

        key_list = self.q_table.keys()
        numSParam = sensor.getNumParam()
        s = Q_learning.discretize(sensor)
        matchingKey = []
        for key in key_list:
            if key[0:numSParam] == s:
                matchingKey.append(key)

        bestQ = 0
        bestKey = []
        for key in matchingKey:
            q = self.q_table[key]
            if q > bestQ:
                    bestKey = []  # clear current best list
                    bestQ = q
                    bestKey.append(key)
            elif q == bestQ:
                bestKey.append(key)

        if len(bestKey) == 0:
            return Q_learning.getRandomMotor(), bestQ
        elif len(bestKey) > 1:
            i = random.randint(0, len(bestKey)-1)

            return self.__getMotor(bestKey[i][numSParam:len(bestKey[i])]), bestQ
        else:
            return self.__getMotor(bestKey[0][numSParam:len(bestKey[0])]), bestQ


    def getRandomMotor():
        val = []
        bounds = Motor.Motor.getBound()
        for bound in bounds:
            val.append(random.uniform(bound[0], bound[1]))

        return Motor.Motor(val)
    getRandomMotor = staticmethod(getRandomMotor)

'''
# Test Code
learner = Q_learning()
sensor = Sensor.Sensor([60.0, 2.0, 100])
motor = Motor.Motor([20.0, -1])
learner.addQ(sensor, motor, 3)
motor2 = Motor.Motor([20.0, 1])
print learner.getQ(sensor, motor2)
print learner.getBestMotor(sensor).getParam()
'''