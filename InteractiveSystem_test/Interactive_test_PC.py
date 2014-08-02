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

    # interactive code
    led_period = 0
    new_sample_received = True
    led_on = [0]*len(serial_num_list)
    sensor_outputs = [-1]*len(serial_num_list)
    while True:


        try:
            # Teensy_selected = int(raw_input("\nEnter the Teensy number: "))
            # Teensy_indicator_led_on = int(raw_input("0 for LED off and 1 for LED on: "))
            # Teensy_indicator_led_period = int(raw_input("Blinking period (ms): "))

            Teensy_selected = -1
            Teensy_indicator_led_on = led_on
            Teensy_indicator_led_period = int(led_period) * 50
            led_period += 0.001
            led_period = led_period % 10
            print("\n<<< LED period >>> " + str(Teensy_indicator_led_period))

        except ValueError:
            print("Invalid input!")
            continue

        start_time = clock()

        # one specific Teensy device selected
        if 0 <= Teensy_selected < len(serial_num_list):

            Teensy_thread_list[Teensy_selected].lock.acquire()
            Teensy_thread_list[Teensy_selected].inputs_sampled_event.clear()
            Teensy_thread.print_to_term("main thread: lock acquired 1")

            try:
                Teensy_thread_list[Teensy_selected].param.set_indicator_led_on(Teensy_indicator_led_on[Teensy_selected])
                Teensy_thread_list[Teensy_selected].param.set_indicator_led_period(Teensy_indicator_led_period)
                Teensy_thread_list[Teensy_selected].param_updated_event.set()
            except Exception as e:
                print(str(e))
            finally:
                Teensy_thread_list[Teensy_selected].lock.release()
                Teensy_thread_list[Teensy_selected].print_to_term("main thread: lock released 1")

        # selected all Teensy devices
        elif Teensy_selected == -1:
            Teensy_thread_id = 0
            for Teensy_thread in Teensy_thread_list:
                Teensy_thread.lock.acquire()
                Teensy_thread.inputs_sampled_event.clear()
                Teensy_thread.print_to_term("main thread: lock acquired 1")

                try:
                    Teensy_thread.param.set_indicator_led_on(Teensy_indicator_led_on[Teensy_thread_id])
                    Teensy_thread.param.set_indicator_led_period(Teensy_indicator_led_period)
                    Teensy_thread.param_updated_event.set()
                except Exception as e:
                    print(str(e))
                finally:
                    Teensy_thread.lock.release()
                    Teensy_thread.print_to_term("main thread: lock released 1")
                Teensy_thread_id += 1
        else:
            print('The selected Teensy device does not exist!')
            continue


        # print sensor output

        new_sample_received = False

        # one specific Teensy device selected
        if 0 <= Teensy_selected < len(serial_num_list):

            new_sample_received = Teensy_thread_list[Teensy_selected].inputs_sampled_event.wait(0.005)
            if new_sample_received:
                #print("New sample received")
                Teensy_thread_list[Teensy_selected].inputs_sampled_event.clear()

                try:
                    sensor_outputs[Teensy_selected] = Teensy_thread_list[Teensy_selected].param.get_input_state('analog_0_state')
                except Exception as e:
                    print(str(e))
            else:
                #print("No new sample received")
                pass

        # selected all Teensy devices
        elif Teensy_selected == -1:
            Teensy_thread_id = 0
            for Teensy_thread in Teensy_thread_list:

                this_new_sample_received = Teensy_thread.inputs_sampled_event.wait(timeout=0.005)
                if this_new_sample_received:
                    Teensy_thread.inputs_sampled_event.clear()

                    try:
                        sensor_outputs[Teensy_thread_id] = Teensy_thread.param.get_input_state('analog_0_state')
                    except Exception as e:
                        print(str(e))
                else:
                    #print("No new sample received")
                    pass
                new_sample_received |= this_new_sample_received
                Teensy_thread_id += 1

        # print if new sample received
        if new_sample_received:
            print("Analog 0 state: " + str(sensor_outputs))

            end_time = clock()
            print("Echo time (ms): " + str((end_time-start_time)*1000))

            for i in range(len(sensor_outputs)):
                led_on[i] = (sensor_outputs[i] > 850)

    for t in Teensy_thread_list:
        t.join()

