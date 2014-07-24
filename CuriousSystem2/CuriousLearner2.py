import random
import numpy as np
import matplotlib.pyplot as plt
import sys

class CuriousLearner2():

    greed = 0.1
    learnRate = 0.1
    gamma = 0.5
    degrade_rate = 1.0  #0.99


    def __init__(self, fea_dim, cmd_dim, fea_num, cmd_num):

        # get to know the dimensions of features and commands
        self.fea_dim = fea_dim
        self.cmd_dim = cmd_dim
        self.fea_num = fea_num
        self.cmd_num = cmd_num

        if (fea_dim > 1):
            print("Error! CuriousLearner2 only support fea_dim = 1")
            sys.exit()
        elif (cmd_dim > 1):
            print("Error! CuriousLearner2 only support cmd_dim = 1")
            sys.exit()

        # instantiate the q-table
        self.q_table = np.zeros((self.fea_num, self.cmd_num))



    def select_action(self, state):

        # bound the state
        state = int(round(min(max(0, state[0]), self.fea_num-1)))

        # choose an random action "greed" percent of the time
        k = random.random()
        if k < CuriousLearner2.greed:
            print("Chose a random output")
            cmd = random.randint(0, self.cmd_num-1)
            return np.array([cmd])
        else:
            # get the optimal action
            optimal_action, bestq = self.__get_optimal_action(state)
            #print("Best Q: " + str(bestq))
            return np.array([optimal_action])


    def update_q_table(self, state_0, action_0, state_1, reward):

        # bound the values
        state_0 = int(round(min(max(0, state_0[0]), self.fea_num-1)))
        state_1 = int(round(min(max(0, state_1[0]), self.fea_num-1)))
        action_0 = int(round(min(max(0, action_0[0]), self.cmd_num-1)))

        # calculate the change in q
        delta_q = CuriousLearner2.learnRate\
                  * (reward + CuriousLearner2.gamma*(self.__estimate_future_reward(state_1)) - self.q_table[state_0][action_0])

        self.q_table[state_0][action_0] += delta_q
        self.q_table *= CuriousLearner2.degrade_rate


    def __estimate_future_reward(self, state1):
        # bound the values
        state1 = min(max(0, state1), self.fea_num-1)

        _, best_q = self.__get_optimal_action(state1)
        return best_q

    def __get_optimal_action(self, state):
        # bound the values
        state = min(max(0, state), self.fea_num-1)

        best_q = self.q_table[state].max()
        best_action = np.where(self.q_table[state] == self.q_table[state].max())[0]

        if len(best_action) > 0:
            k = random.randint(0, len(best_action)-1)
            action_selected = best_action[k]

        return action_selected, best_q

    def get_state_action_with_highest_q(self):

        best_q_index_flat = self.q_table.argmax()
        return np.unravel_index(best_q_index_flat, self.q_table.shape)

    def get_action_with_highest_q(self, state):

        best_q_index_flat = self.q_table[state].argmax()
        return np.unravel_index(best_q_index_flat, self.q_table[state].shape)

    def get_q_column(self, state0):
        # bound the values
        state0 = int(min(max(0, state0), self.fea_num-1))
        q_col = self.q_table[state0, :]

        return q_col

    @staticmethod
    def test():

        learner = CuriousLearner2(1, 1, 10, 10)
        state0_history = []
        action_history = []
        state1_history = []

        state0 = np.array([7])
        for i in range(100000):
            action = learner.select_action(state0)
            state1 = np.array([round(max(min(state0[0] + action - 5, learner.fea_num-1), 0))])


            if state1[0] < 5:
                reward = state1[0]**2 - 5

            else:
                reward = (10-state1[0])**2 - 5

            print("State0: " + str(state0))
            print("Action: " + str(action))
            print("State1: " + str(state1))
            print("Reward: " + str(reward) + "\n")
            state0_history.append(state0[0])
            action_history.append(action[0])
            state1_history.append(state1[0])

            learner.update_q_table(state0, action, state1, reward)
            state0 = state1

        plt.figure(1)
        plt.hist2d(state0_history, action_history)
        plt.colorbar()
        plt.figure(2)
        matrix = np.transpose(np.matrix(learner.q_table))
        plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.ocean,
                    extent=(0.0,np.shape(matrix)[0],0.0,np.shape(matrix)[1]))
        plt.colorbar()
        print (matrix)
        plt.show()

#CuriousLearner2.test()