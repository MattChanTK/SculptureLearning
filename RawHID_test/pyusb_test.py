import usb.core
import usb.util
import sys

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
while loopCount < 100:
    ep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_OUT)

    assert ep is not None

    # write the data
    ep.write('test')


    ep = usb.util.find_descriptor(
        intf,
        # match the first OUT endpoint
        custom_match = \
        lambda e: \
            usb.util.endpoint_direction(e.bEndpointAddress) == \
            usb.util.ENDPOINT_IN)

    assert ep is not None
    try:
        print("release device")
        usb.util.release_interface(dev, intf)
        print("claiming device")
        usb.util.claim_interface(dev, intf)
        print(ep.read(64, 2000))
    except:
        print("Couldn't claim interface!")

    loopCount += 1
