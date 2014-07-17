import usb.core
import usb.util
import sys
from time import clock
from time import sleep




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
    usb.util.release_interface(dev, intf)
   # print("claiming device")
    usb.util.claim_interface(dev, intf)
    try:

        data = ep.read(byte_num, timeout)

    except usb.core.USBError:
        print("Timeout! Couldn't read anything")
        data = None

    return data

def talk_to_Teensy(dev, intf, out_msg, timeout=10):

    # print("release device")
    usb.util.release_interface(dev, intf)
    # print("claiming device")
    usb.util.claim_interface(dev, intf)

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
        print("Timeout! Couldn't write")


def print_data(data):
    if data:
        i = 0
        while i < len(data):
            char = chr(data[i])
            print(char),
            i +=1

        print('\n')


def listen_and_respond_test(vendorID, productID, loop_num=1000):
    # find our device
    dev = usb.core.find(idVendor=vendorID, idProduct=productID)

    # was it found?
    if dev is None:
        raise ValueError('Device not found')

    # set the active configuration. With no arguments, the first
    # configuration will be the active one
    dev.set_configuration()

    # get an endpoint instance
    cfg = dev.get_active_configuration()

    interface = usb.util.find_descriptor(cfg, find_all=True)
    intf = interface[0]

    loop_count = 0

    while loop_count < loop_num:

        data = listen_to_Teensy(dev, intf)

        print_data(data)

        if data:
            #intf = interface[0]

            # write the data
            out_string = "I heard you Teensy! " + str(loop_count)
            out_msg = out_string.encode(encoding='UTF-8')
            padding = ' ' *(64 - len(out_msg))
            out_msg = out_msg + padding

            print("Sent: " + out_string)
            talk_to_Teensy(dev, intf, out_msg)

            # read reply
            data = listen_to_Teensy(dev, intf)
            print_data(data)



        loop_count += 1

if __name__ == '__main__':

    listen_and_respond_test(vendorID=0x16C0, productID=0x0486, loop_num=100000)