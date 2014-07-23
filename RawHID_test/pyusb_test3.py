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

packet_size_in = 64
packet_size_out = 64

def setpriority(pid=None,priority=1):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process but can take any valid process ID. """

    import win32api,win32process,win32con

    priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])

def listen_to_Teensy(dev, intf, timeout=100, byte_num=64):

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

def talk_to_Teensy(dev, intf, out_msg, timeout=10):

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


def print_data(data, serialNum=u'N/A'):
    if data:
        i = 0
        print("Serial Number: " + str(serialNum))
        print("Number of byte: " + str(len(data)))
        while i < len(data):
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
    while loop_count < loop_num:


        data = listen_to_Teensy(dev, intf, timeout=0, byte_num=packet_size_in)


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
                talk_to_Teensy(dev, intf, out_msg, timeout=0)

                # read reply
                data = listen_to_Teensy(dev, intf, timeout=0, byte_num=packet_size_in)

                if data:
                    #print("Replied: "),
                    save_data(resultQueue, data, serialNumber)
                else:
                    pass
                    #print("Received no reply.")


        loop_count += 1

def find_teensy_serial_number(vendorID=0x16C0, productID=0x0486):

    # find our device
    dev_iter = usb.core.find(find_all=True, idVendor=vendorID, idProduct=productID)

    serialNum = []
    for iter in dev_iter:
        serialNum.append(iter.serial_number)

    return tuple(serialNum)


if __name__ == '__main__':


    changePriority.SetPriority(changePriority.Priorities.ABOVE_NORMAL_PRIORITY_CLASS)

    vendor_id = 0x16C0
    product_id = 0x0486
    serial_num_list = find_teensy_serial_number(vendorID=vendor_id, productID=product_id)

    result_queue = Queue.Queue()
    thread_list = []
    for serial_num in serial_num_list:
        ids = ()
        t = threading.Thread(target=listen_and_respond_test, args=(result_queue, vendor_id, product_id, serial_num, 1000))
        thread_list.append(t)
        t.daemon = False
        t.start()

    for t in thread_list:
        t.join()
        while not result_queue.empty():
            result = result_queue.get()
            print_data(result[1], serialNum=result[0])


