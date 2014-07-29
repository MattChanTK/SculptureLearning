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

packet_size_in = 64
packet_size_out = 64

def compose_msg(blinkPeriod):

    # unique id for each message
    front_id_dec = random.randint(0, 255)
    back_id_dec = random.randint(0, 255)
    front_id = struct.pack('c', chr(front_id_dec))
    back_id = struct.pack('c', chr(back_id_dec))

    # the actual message
    try:
        out_string = struct.pack('l', blinkPeriod)
    except:
        out_string = struct.pack('l', -1)

    # fill up the empty spots
    padding = chr(0)*(packet_size_out - len(out_string) - 2)

    # stitch the message together
    out_msg = bytearray(front_id + out_string + padding + back_id)

    return out_msg, front_id_dec, back_id_dec

def listen_to_Teensy(intf, timeout=100, byte_num=64):

    ep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_IN)

    assert ep is not None

   # print("release device")
   # usb.util.release_interface(dev, intf)
   # print("claiming device")
   # usb.util.claim_interface(dev, intf)

    try:
        data = ep.read(byte_num, timeout)

    except usb.core.USBError:
        #print("Timeout! Couldn't read anything")
        data = None

    return data


def talk_to_Teensy(intf, out_msg, timeout=10):

    # print("release device")
    # usb.util.release_interface(dev, intf)
    # print("claiming device")
    # usb.util.claim_interface(dev, intf)

    ep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)

    assert ep is not None

    try:
        ep.write(out_msg, timeout)
    except usb.core.USBError:
        pass
        #print("Timeout! Couldn't write")


def print_data(data, serialNum=u'N/A', raw_dec=False):
    if data:
        i = 0
        print("Serial Number: " + str(serialNum))
        print("Number of byte: " + str(len(data)))
        while i < len(data):
            if raw_dec:
                char = int(data[i])
            else:
                char = chr(data[i])
            print(char),
            i +=1

        print('\n')


def save_data(queue, data, serial_num):
    if data and queue:
        queue.put([serial_num, copy.copy(data)])


def listen_and_respond_test(resultQueue, vendorID, productID, serialNumber, loop_num=1000):
    # find our device
    dev = usb.core.find(idVendor=vendorID, idProduct=productID, serial_number=serialNumber)
    # was it found?
    if dev is None:
        raise ValueError('Device not found')

    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    dev.set_configuration()

    # get an endpoint instance
    cfg = dev.get_active_configuration()

    interface_iter = usb.util.find_descriptor(cfg, find_all=True)
    interface = []
    for iter in interface_iter:
        interface.append(iter)
    intf = interface[0]

    loop_count = 0

    listen_string = "Hello PC! This is Teensy"
    listen_msg = bytearray(listen_string)[:packet_size_in]
    listen_reply_string = "Teensy heard an echo"
    listen_reply_msg = bytearray(listen_reply_string)[:packet_size_in]
    while loop_count < loop_num:


        data = listen_to_Teensy( intf, timeout=0, byte_num=packet_size_in)


        if data:
            correct_msg = True
            for i in range(len(listen_msg)):
                correct_msg &= (listen_msg[i] == data[i])


            if correct_msg:
                # write the data
                out_string = str(loop_count) + " I heard you Teensy!"
                padding = ' ' *(packet_size_out - len(out_string))
                out_msg = bytearray((out_string + padding)[:packet_size_out])

                #print("Sent: " + out_string + padding)
                talk_to_Teensy(intf, out_msg, timeout=0)

                # read reply
                data = listen_to_Teensy(intf, timeout=0, byte_num=packet_size_in)

                if data:
                    for i in range(len(listen_reply_msg)):
                        correct_msg &= (listen_reply_msg[i] == data[i])

                    if correct_msg:
                        #print("Replied: "),
                        save_data(resultQueue, data, serialNumber)


        loop_count += 1


def interactive_test(vendorID, productID, serialNumber):

    # find our device
    dev = usb.core.find(idVendor=vendorID, idProduct=productID, serial_number=serialNumber)
    # was it found?
    if dev is None:
        raise ValueError('Device not found')

    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    dev.set_configuration()

    # get an endpoint instance
    cfg = dev.get_active_configuration()

    interface_iter = usb.util.find_descriptor(cfg, find_all=True)
    interface = []
    for iter in interface_iter:
        interface.append(iter)
    intf = interface[0]


    while(True):

        print(str(serial_num) + ": "),
        try:
            blinkPeriod = long(raw_input())
        except ValueError:
            blinkPeriod = -1

        # compose the data
        out_msg, front_id, back_id = compose_msg(blinkPeriod=blinkPeriod)

        # sending the data
        print("---Sent---")
        print_data(out_msg, serialNumber, raw_dec=True)

        received_reply = False
        talk_to_Teensy(intf, out_msg, timeout=0)

        # waiting for reply
        data = listen_to_Teensy(intf, timeout=100, byte_num=packet_size_in)

        invalid_reply_counter  = 0
        while data and received_reply is False:
            # check if reply matches sent message
            if data[0] == front_id and data[-1] == back_id:

                print("---Received Reply---")
                print_data(data, serialNum=serialNumber, raw_dec=True)
                #print(struct.unpack_from('l', data[1:-1]))
                received_reply = True
            else:
                print("......Received invalid reply......")
                print_data(data, serialNum=serialNumber, raw_dec=True)
                #print(struct.unpack_from('l', data[1:-1]))

            invalid_reply_counter += 1
            if invalid_reply_counter > 5:
                print("......Number of invalid replies exceeded 5! Stopped trying......")
                break




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

    Teensy_thread_list = []
    Teensy_id = 0
    for serial_num in serial_num_list:
        print("Teensy " + str(Teensy_id) + " --- " + str(serial_num))
        Teensy_id += 1
        t = threading.Thread(target=interactive_test, args=(vendor_id, product_id, serial_num))
        Teensy_thread_list.append(t)
        t.daemon = False
        t.start()



    for t in Teensy_thread_list:
        t.join()

