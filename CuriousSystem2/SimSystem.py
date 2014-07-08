import numpy as np

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
