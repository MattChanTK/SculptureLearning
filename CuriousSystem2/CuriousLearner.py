import random
import numpy as np
import RLtoolkit.tiles as tiles


class CuriousLearner():

    greed = 0.0
    learnRate = 0.35
    gamma = 0.75

    tiling_num = 2**8
    partition_size = 2**4
    memory_size = min(tiling_num*partition_size**2, 512000)


    def __init__(self, fea_num, cmd_num):
        self.q_table = dict()
        self.past_action = dict()

        # get to know the dimensions of features and commands
        self.fea_num = fea_num
        self.cmd_num = cmd_num

    def select_action(self, state):

        # choose an random action "greed" percent of the time
        k = random.random()
        if k < CuriousLearner.greed:
            cmd = np.zeros(self.cmd_num)
            for i in range(self.cmd_num):
                cmd[i] = random.random()*CuriousLearner.partition_size
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

    def update_past_action(self, state, action):
        state_id = tiles.tiles(CuriousLearner.tiling_num, CuriousLearner.memory_size, state)

        for i in range(CuriousLearner.tiling_num):
            if state_id[i] not in self.past_action:
                self.past_action[state_id[i]] = []
            self.past_action[state_id[i]].append(action)

    def __estimate_future_reward(self, state):
        return 0

    def __get_optimal_action(self, state):

        state_id = tiles.tiles(CuriousLearner.tiling_num, CuriousLearner.memory_size, state)
        q_max = [None]*CuriousLearner.tiling_num
        action_max = [None]*CuriousLearner.tiling_num

        for i in range(CuriousLearner.tiling_num):
            if state_id[i] in self.past_action:
                action_list = self.past_action[state_id[i]]

                # get the action with the max q that has already been tried
                for action in action_list:
                    q_id = tiles.tiles(CuriousLearner.tiling_num, CuriousLearner.memory_size, state + action)
                    q = 0
                    for j in range(CuriousLearner.tiling_num):
                        q += self.q_table[q_id[j]]

                    # record the max q and its associated action
                    if q_max[i] is None:
                        q_max[i] = q
                        action_max[i] = action
                    else:
                        if (q > q_max[i]):
                            q_max[i] = q
                            action_max[i] = action

            # if no action has been done before or the best q is less than or equal to 0
            if q_max[i]is None or q_max[i] <= 0:
                q_max[i] = 0
                action_max[i] = random.random()*CuriousLearner.partition_size
            else:
                action_max[i]

        return np.sum(action_max)/CuriousLearner.tiling_num




learner = CuriousLearner(1, 1)
for i in range(10):
    state = (10,)
    action = (1000,)
    learner.update_past_action(state, action)
    learner.update_q_table(state, action, 5, 4)
print learner.select_action((10,))

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