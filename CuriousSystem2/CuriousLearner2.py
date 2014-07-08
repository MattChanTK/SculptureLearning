import random
import numpy as np

class CuriousLearner2():

    greed = 0.10
    learnRate = 0.10
    gamma = 0.75

    state_num = 10
    action_num = 10


    def __init__(self, fea_num, cmd_num):
        self.q_table = np.zeros((CuriousLearner2.state_num, CuriousLearner2.action_num))

        # get to know the dimensions of features and commands
        self.fea_num = fea_num
        self.cmd_num = cmd_num

    def select_action(self, state):

        # choose an random action "greed" percent of the time
        k = random.random()
        if k < CuriousLearner2.greed:
            cmd = random.random()*CuriousLearner2.action_num
            return cmd
        else:
            return self.__get_optimal_action(state)


    def update_q_table(self, state_0, action_0, state_1, reward):

        delta_q = CuriousLearner2.learnRate\
                  * (reward + CuriousLearner2.gamma*(self.__estimate_future_reward(state_1) - self.q_table[state_0][action_0]))

        self.q_table[state_0][action_0] += delta_q


    def __estimate_future_reward(self, state):
        return 0

    def __get_optimal_action(self, state):


        best_q = self.q_table[state].max()
        best_action = np.where(self.q_table[state] == self.q_table[state].max())[0]

        if len(best_action) > 0:
            k = random.randint(0,len(best_action)-1)
            action_selected = best_action[k]

        print("Best Q: " + str(best_q))
        print("Action Selected: " + str(action_selected))

        return best_action[k]




learner = CuriousLearner2(1, 1)

state0 = 9
for i in range(1000):
    action = learner.select_action(state0)
    state1 = max(min(state0 + action - 5, CuriousLearner2.state_num-1), 0)


    if state1 < 5:
        reward = state1**2
    else:
        reward = (10-state1)**2

    print("State1: " + str(state1))
    print("Reward: " + str(reward))
    learner.update_q_table(state0, action, state1, reward)
    state0 = state1

