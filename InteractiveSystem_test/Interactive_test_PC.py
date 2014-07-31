import usb.core
import usb.util

import sys
from time import clock
from time import sleep
import copy
import array
import math
import threading
import Queue
import changePriority
import struct
import random

import TeensyInterface as ti

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
        except Exception, e:
            print(str(e))

    # interactive code
    while True:

        try:
            Teensy_selected = int(raw_input("\nEnter the Teensy number: "))
            Teensy_indicator_led_on = int(raw_input("0 for LED off and 1 for LED on: "))
            Teensy_indicator_led_period = int(raw_input("Blinking period (ms): "))

        except ValueError:
            print("Invalid input!")
            continue


        try:
            if 0 <= Teensy_selected < len(serial_num_list):

                Teensy_thread_list[Teensy_selected].lock.acquire()
                Teensy_thread_list[Teensy_selected].param.set_indicator_led_on(Teensy_indicator_led_on)
                Teensy_thread_list[Teensy_selected].param.set_indicator_led_period(Teensy_indicator_led_period)
                Teensy_thread_list[Teensy_selected].param_updated_event.set()
                Teensy_thread_list[Teensy_selected].lock.release()

            elif Teensy_selected == -1:

                for Teensy_thread in Teensy_thread_list:
                    Teensy_thread.lock.acquire()
                    Teensy_thread.print_to_term("main thread: lock acquired")
                    Teensy_thread.param.set_indicator_led_on(Teensy_indicator_led_on)
                    Teensy_thread.param.set_indicator_led_period(Teensy_indicator_led_period)
                    Teensy_thread.param_updated_event.set()
                    Teensy_thread.lock.release()
                    Teensy_thread.print_to_term("main thread: lock released")

            else:
                raise ValueError('The selected Teensy device does no exist!')

        except Exception, e:
            print(str(e))

        # print sensor output
        sensor_outputs = []
        try:
            for Teensy_thread in Teensy_thread_list:
                if Teensy_thread.inputs_sampled_event.wait(timeout=0.01):
                    Teensy_thread.inputs_sampled_event.clear()
                    Teensy_thread.lock.acquire()
                    Teensy_thread.print_to_term("main thread: lock acquired")
                    sensor_outputs.append(Teensy_thread.param.analog_0_state)
                    Teensy_thread.lock.release()
                    Teensy_thread.print_to_term("main thread: lock released")
            print("Analog 0 state: " + str(sensor_outputs))
        except Exception, e:
            print(str(e))


    for t in Teensy_thread_list:
        t.join()

