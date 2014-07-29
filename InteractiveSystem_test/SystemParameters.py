import struct
import sys

class SystemParameters():

    msg_length = 64

    def __init__(self):
        self.indicator_led_on = False
        self.indicator_led_period = 2**16 - 1

    def set_indicator_led_on(self, state):
        if isinstance(state, bool):
            self.indicator_led_on = state
        else:
            raise TypeError("LED state must either be 'True' or 'False'")

    def set_indicator_led_period(self, period):
        if isinstance(period, int):
            if period > 2**16 - 1 or period < 0:
                raise TypeError("LED period must either be positive and less than " + str(2**16))
            self.indicator_led_period = period
        else:
            raise TypeError("LED period must be an integer")


    def compose_message_content(self):

        # create an 64 bytes of zeros
        msg = bytearray(chr(0)*SystemParameters.msg_length)

        # byte 0 and byte 63: the msg signature; left as 0 for now

        # byte 1: whether the indicator LED on or off
        msg[1] = self.indicator_led_on

        # byte 2 to 4: blinking frequency of the LED
        msg[2:4] = struct.pack('H', self.indicator_led_period)

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
            print(char),
            i += 1

        print('\n')


if __name__ == '__main__':
    s = SystemParameters()
    s.set_indicator_led_on(True)
    s.set_indicator_led_period(65535)
    print_data(s.compose_message_content(), raw_dec=True)