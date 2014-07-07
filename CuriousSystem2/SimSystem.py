import numpy as np

class SimSystem():

    def __init__(self, input_num, output_num):
        self.input = np.zeros(input_num)
        self.output = np.zeros(output_num)

    def _get_input_num(self):
        return np.size(self.input)

    def _get_output_num(self):
        return np.size(self.output)

    def __extract_feature(self):

        feature = self.input

        return feature

    def __decode_command(self, command):
        self.output = command

    def simulate(self, command):

        # decode the command and invoke the actuator
        self.__decode_command(command)

        # simulate the system
        self.input = self.output*2

        # return the features
        return self.__extract_feature()
