import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=0x16C0, idProduct=0x0486)
#dev = usb.core.find(find_all=True)


# was it found?
if dev is None:
    raise ValueError('Device not found')


    print("but we need to detach kernel driver")
    dev.detach_kernel_driver(0)
    print("claiming device")
    usb.util.claim_interface(dev, 0)

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()



ep = []
for cfg in dev:
    for i in cfg:
        for e in i:
            ep.append(e.bEndpointAddress)

dev.write(ep[1], 'test')
#data = dev.read(0x83, 64)


#print(data)
