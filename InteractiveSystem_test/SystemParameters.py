import struct
import sys

class SystemParameters():

    msg_length = 64

    def __init__(self):

        #==== outputs ====
        self.output_param = dict()
        # ---defaults---
        self.output_param['indicator_led_on'] = False
        self.output_param['indicator_led_period'] = 2**16 - 1
        #self.indicator_led_on = False
        #self.indicator_led_period = 2**16 - 1

        #==== inputs ====
        self.input_state = dict()
        self.input_state['analog_0_state'] = 0
        #self.analog_0_state = 0

    def get_input_state(self, state_type):
        if isinstance(state_type, str):
            if state_type in self.input_state:
                return self.input_state[state_type]
            else:
                raise ValueError(state_type + " does not exist!")
        else:
            raise TypeError("'State type' must be a string!")

    def set_output_param(self, param_type, param_val):
        if isinstance(param_type, str):
            if param_type in self.output_param:
                if param_type == 'indicator_led_on':
                    self.set_indicator_led_on(param_val)
                elif param_type == 'indicator_led_period':
                    self.set_indicator_led_period(param_val)
                else:
                    #warning! this function does not do type error check on values
                    self.output_param[param_type] = param_val
            else:
                raise ValueError(param_type + " does not exist!")
        else:
            raise TypeError("'Parameter type' must be a string!")

    def set_indicator_led_on(self, state):
        if isinstance(state, bool):
            self.output_param['indicator_led_on'] = state
        elif state == 0:
            self.output_param['indicator_led_on'] = False
        elif state == 1:
            self.output_param['indicator_led_on'] = True
        else:
            raise TypeError("LED state must either be 'True' or 'False'")

    def set_indicator_led_period(self, period):
        if isinstance(period, int):
            if period > 2**16 - 1 or period < 0:
                raise TypeError("LED period must either be positive and less than " + str(2**16))
            self.output_param['indicator_led_period'] = period
        else:
            raise TypeError("LED period must be an integer")




    def parse_message_content(self, msg):

        # byte 0 and byte 63: the msg signature; can ignore

        # byte 1: analog 0 state
        self.input_state['analog_0_state'] = struct.unpack_from('H', msg[1:3])[0]

    def compose_message_content(self):

        # create an 64 bytes of zeros
        msg = bytearray(chr(0)*SystemParameters.msg_length, 'utf-8')

        # byte 0 and byte 63: the msg signature; left as 0 for now

        # byte 1: whether the indicator LED on or off
        msg[1] = self.output_param['indicator_led_on']

        # byte 2 to 4: blinking frequency of the LED
        msg[2:4] = struct.pack('H', self.output_param['indicator_led_period'])

        return msg

def print_data(data, raw_dec=False):
    if data:
        i = 0
        print("Number of byte: " + str(len(data)))
        while i < len(data):
            if raw_dec:
                char = int(data[i])
            else:
                char = chr(data[i])
            print(char, end=" ")
            i += 1

        print('\n')


if __name__ == '__main__':
    s = SystemParameters()
    s.set_indicator_led_on(True)
    s.set_indicator_led_period(65535)
    print_data(s.compose_message_content(), raw_dec=True)