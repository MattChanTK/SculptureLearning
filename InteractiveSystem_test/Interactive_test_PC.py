import usb.core
import usb.util

import sys
from time import clock
from time import sleep
import copy
import array
import math
import threading
import changePriority
import struct
import random

import TeensyInterface as ti
from HardcodedBehaviours import HardcodedBehaviours as cmd
#from InteractiveCmd import InteractiveCmd as cmd


packet_size_in = 64
packet_size_out = 64

def find_teensy_serial_number(vendorID=0x16C0, productID=0x0486):

    # find our device
    dev_iter = usb.core.find(find_all=True, idVendor=vendorID, idProduct=productID)

    serialNum = []
    for iter in dev_iter:
        serialNum.append(iter.serial_number)

    return tuple(serialNum)


if __name__ == '__main__':

    # change priority of the the Python process to HIGH
    changePriority.SetPriority(changePriority.Priorities.HIGH_PRIORITY_CLASS)

    # filter out the Teensy with vendor ID and product ID
    vendor_id = 0x16C0
    product_id = 0x0486

    # find all the Teensy
    serial_num_list = find_teensy_serial_number(vendorID=vendor_id, productID=product_id)
    print("Number of Teensy devices found: " + str(len(serial_num_list)))

    # creating Teensy interface threads
    Teensy_thread_list = []
    Teensy_id = 0
    for serial_num in serial_num_list:
        print("Teensy " + str(Teensy_id) + " --- " + str(serial_num))
        Teensy_id += 1

        # create a new thread for communicating with
        try:
            Teensy_thread = ti.TeensyInterface(vendor_id, product_id, serial_num, print_to_term=False)
            Teensy_thread_list.append(Teensy_thread)
        except Exception as e:
            print(str(e))



    led_period = 0
    new_sample_received = True
    led_on = [0]*len(serial_num_list)
    sensor_outputs = [-1]*len(serial_num_list)

    # interactive code
    #behaviours = cmd.HardcodedBehaviours(Teensy_thread_list)
    behaviours = cmd(Teensy_thread_list)
    behaviours.run()

    for t in Teensy_thread_list:
        t.join()

    print("All threads terminated")

