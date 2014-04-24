from setup import*
import Sensor
import Motor
import random


class Q_learning():

    greed = 0.10
    learnRate = 0.35
    gamma = 1.0


    def __init__(self, sensor, motor):

        # Q value (weight for each action)
        self.q_table = dict()

        # mapping sensor values into discrete set of states
        self.s_state = []
        if sensor.isSimple():
            self.s_state = [sensor.getSimpleStates()]
        else:
            bounds = Sensor.Sensor.getBound()
            division_s = num_s_division  # number of sensor states per dimension
            for i in range(0, len(bounds)):
                discrete_states = frange(bounds[i][0],  bounds[i][1], division_s)
                self.s_state.append(discrete_states)
                print("Sensor States[" + str(i) + "]: " + str(discrete_states))

        self.s_state = tuple(self.s_state)


        # mapping motor values into discrete set of states
        self.m_state = []
        if motor.isSimple():
            self.m_state = [motor.getSimpleStates()]
        else:
            bounds = Motor.Motor.getBound()
            division_m = num_m_division  # number of sensor states per dimension
            for i in range(0, len(bounds)):
                # ensuring equal number of plus and minuses
                discrete_states = frange(0,  bounds[i][1], int(division_m/2) + 1)
                negState = np.array(discrete_states[1:])
                negState *= -1
                discrete_states = list(discrete_states) + negState.tolist()
                discrete_states.sort()
                self.m_state.append(discrete_states)
                discrete_states = tuple(discrete_states)
                print("Motor States[" + str(i) + "]: " + str(discrete_states))
        self.m_state = tuple(self.m_state)

    def discretize(input, states):
        # sensor/motor state per dimension
        s = [0]*input.getNumParam()

        # check if it's a sensor input or motor input
        state = states

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
            motorVal.append(self.m_state[i][input[i]])
        return Motor.Motor(motorVal)

    def getQ(self, sensor, motor):

        if sensor.isSimple():
            s = sensor.getParam()
        else:
            s = Q_learning.discretize(sensor, self.s_state)

        if motor.isSimple():
            m = motor.getParam()
        else:
            m = Q_learning.discretize(motor, self.m_state)

        if s + m in self.q_table:
            return self.q_table[s + m]
        else:
            return 0

    def addQ(self, sensor, motor, q_val):
        if sensor.isSimple():
            s = sensor.getParam()
        else:
            s = Q_learning.discretize(sensor, self.s_state)
        if motor.isSimple():
            m = motor.getParam()
        else:
            m = Q_learning.discretize(motor, self.m_state)

        self.q_table[s+m] = q_val

    def getBestMotor(self, sensor):

        # at random choose an random action
        k = random.random()
        if k < Q_learning.greed:
            motor = self.getRandomMotor()
            return motor, self.getQ(sensor, motor)

        key_list = self.q_table.keys()
        numSParam = sensor.getNumParam()
        if sensor.isSimple():
            s = sensor.getParam()
        else:
            s = Q_learning.discretize(sensor, self.s_state)
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
        print("Best Q: " + str(bestQ))
        if len(bestKey) == 0:
            return self.getRandomMotor(), bestQ
        elif len(bestKey) > 1:
            i = random.randint(0, len(bestKey)-1)

            return self.__getMotor(bestKey[i][numSParam:len(bestKey[i])]), bestQ
        else:
            return self.__getMotor(bestKey[0][numSParam:len(bestKey[0])]), bestQ


    def getRandomMotor(self, simple=False):

        val = []
        for i in range(0,len(self.m_state)):
            val.append(self.m_state[i][random.randint(0, len(self.m_state[i])-1)])

        return Motor.Motor(val, simple)


# # Test Code
# learner = Q_learning()
# sensor = Sensor.Sensor([60.0, 2.0, 100])
# motor = Motor.Motor([20.0, -1])
# learner.addQ(sensor, motor, 3)
# motor2 = Motor.Motor([20.0, 1])
# print learner.getQ(sensor, motor2)
# print learner.getBestMotor(sensor).getParam()
