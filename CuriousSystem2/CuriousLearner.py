import random
import numpy as np
import RLtoolkit.tiles as tiles


class CuriousLearner():

    greed = 0.25
    learnRate = 0.35
    gamma = 0.75

    tiling_num = 2**8
    partition_size = 2**4
    memory_size = min(tiling_num*partition_size**2, 512000)


    def __init__(self, fea_num, cmd_num):
        self.q_table = dict()
        self.optimal_action_table = dict()

        # get to know the dimensions of features and commands
        self.fea_num = fea_num
        self.cmd_num = cmd_num

    def select_action(self, state):

        # choose an random action "greed" percent of the time
        k = random.random()
        if k < CuriousLearner.greed:
            cmd = np.zeros(self.cmd_num)
            for i in range(self.cmd_num):
                cmd[i] = random.random()
            return cmd
        else:
            return self.__get_optimal_action(state)


    def update_q_table(self, state_0, action_0, state_1, reward):

        q0_id = tiles.tiles(CuriousLearner.tiling_num, CuriousLearner.memory_size, state_0 + action_0)

        for i in range(CuriousLearner.tiling_num):
            if q0_id[i] not in self.q_table:
                self.q_table[q0_id[i]] = 0

            delta_q = CuriousLearner.learnRate/CuriousLearner.tiling_num\
                      * (reward + CuriousLearner.gamma*(self.__estimate_future_reward(state_1) - self.q_table[q0_id[i]]))

            self.q_table[q0_id[i]] += delta_q

    def __estimate_future_reward(self, state):
        return 0

    def __get_optimal_action(self, state):
        cmd = np.zeros(self.cmd_num)
        for i in range(self.cmd_num):
            cmd[i] = random.random()
        return cmd


learner = CuriousLearner(1, 1)
for i in range(10):
    learner.update_q_table([10], [10], 5, 4)
print learner.select_action([1])

'''
    def __select_next_action(self, input_state):
        matching_state = []
        cmd_selected = np.zeros(self.cmd_num)

        for state in self.q_table:
            if state[0:self.fea_num] == input_state:
                matching_state.append(state)

        if len(matching_state) > 0:
            highest_q = self.q_table[matching_state[0]]
            highest_states = []
            for state in matching_state:
                q = self.q_table[state]
                if q > highest_q:
                    highest_states = []  # clear current highest states list
                    highest_q = q
                    highest_states.append(state)
                elif q == highest_q:
                    highest_states.append(state)
                else:
                    print("CuriousLearner: Error! \"q\" is not supposed to be less than \"highest_q\"")

            # if more than one possible action with the same q
            if len(highest_states) > 0:
                # randomly select one out of the list of possible candidates
                k = random.randint(0, len(highest_states) - 1)
                cmd_selected = self.q_table[highest_states[k]]
            else:
                print("CuriousLearner: Error! Length of \"highest_states\" is not supposed to be "
                      + str(len(highest_states)))

        else:
            highest_q = 0
            for i in range(self.cmd_num):
                cmd_selected[i] = random.random()
        return cmd_selected, highest_q
'''



'''

float_array = [0.5, 0.5]
num_tiling = 1
memory_size = 512
tiles_array = tiles.tiles(num_tiling, memory_size, float_array)
sum = 0
weight = np.zeros(memory_size)


for j in range(50):
    result = 0

    for i in range(num_tiling):
        result += weight[tiles_array[i]]

    for i in range(num_tiling):
        weight[(tiles_array[i])] += alpha*(target-result)
    print tiles_array
    print result
result = 0

tiles_array = tiles.tiles(num_tiling, memory_size, [0.6, 0.6])
for i in range(num_tiling):
    result += weight[tiles_array[i]]
print tiles_array
print result
print weight


'''