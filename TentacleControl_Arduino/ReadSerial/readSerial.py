__author__ = 'Matthew'

import serial
import time
import datetime

port = serial.Serial('COM4', 9600)

print(port.name)

input = 's'
current_datetime = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
file = open('serial_output_'+current_datetime+'.txt', 'a+')  # append mode
startTime = time.time()
timePassed = 0
while timePassed < 30:

    timePassed = time.time() - startTime
    x = port.read(size=1)  # 1 byte
    if x == b'\t':
        file.write(',')
        print(',', end="")
    elif x == b'\n':
        file.write('\n')
        file.write(str(timePassed)+',')
        print('\n', end="")
        print(timePassed, end=": ")
    elif x == b'\r':
        pass  # ignore
    else:
        file.write(x.decode(encoding='UTF-8'))
        print(x.decode(encoding='UTF-8'), end="")


file.close()

port.close()