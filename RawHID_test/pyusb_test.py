import usb.core
import usb.util
import sys
from time import clock

# find our device
dev = usb.core.find(idVendor=0x16C0, idProduct=0x0486)

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

loopCount = 0

while loopCount < 1000000:
    ep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)

    assert ep is not None
    prev_time = clock()

    # write the data
    out_string = "This is a message from the PC!"
    out_msg = out_string.encode(encoding='UTF-8')
    padding = ' ' *(64-len(out_msg))
    out_msg = out_msg + padding
    ep.write(out_msg)


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
        prev_time = clock()
        data = ep.read(64, 0)

        print(clock() - prev_time)
        prev_time = clock()
        #print(data)

        i = 0
        while i < len(data):
            char = chr(data[i])
            print(char),
            i +=1

        print('\n')
    except usb.core.USBError:
        print("Timeout! Couldn't read anything")

    #print("Couldn't claim interface!")

    loopCount += 1
