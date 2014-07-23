import sys
import numpy as np

import Expert2


class Partition():

    def __init__(self, fea_num, cmd_num):

        # get to know the number of features and commands
        self.fea_num = fea_num
        self.cmd_num = cmd_num

        # instantiate the prediction error chart
        self.error_table = np.ones((fea_num, cmd_num))*sys.float_info.max

        # instantiate an expert in each state-action
        self.expert_table = [[None]*cmd_num]*fea_num
        for fea_row in range(len(self.expert_table)):
            for cmd_col in range(len(self.expert_table[fea_row])):
                self.expert_table[fea_row][cmd_col] = Expert2.Expert2()

    def get_expert(self, state, action):
        return self.expert_table[state][action]

def test():
    p = Partition(10, 10)

#test()