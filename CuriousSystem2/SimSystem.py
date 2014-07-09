import numpy as np
import random

class SimSystem():

    input_num = 1
    output_num = 1

    def __init__(self):
        self.input = np.zeros(SimSystem.input_num)
        self.output = np.zeros(SimSystem.output_num)

    def _get_input_num(self):
        return np.size(self.input)

    def _get_output_num(self):
        return np.size(self.output)

    def __extract_feature(self):

        feature = self.input
        for i in range(len(feature)):
            feature[i] = min(max(0, feature[i]), 9)

        return feature

    def __decode_command(self, command):
        for i in range(len(command)):
            self.output[i] = min(max(0, command[i]), 9)

    def simulate(self):
        # simulate the system
        self.input += self.output-5 + random.randint(-2, 2)

    def read_feature(self):

         # return the features
        return self.__extract_feature()

    def write_command(self, command):

        # decode the command and invoke the actuator
        self.__decode_command(command)

