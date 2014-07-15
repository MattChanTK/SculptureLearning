#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
"""
Handling raw data inputs example
"""
from time import sleep
from msvcrt import kbhit
from time import clock

import pywinusb.hid as hid

prev_time = clock()
def sample_handler(data):
    print(data)

def raw_test():
    # simple test
    # browse devices...
    all_hids = hid.find_all_hid_devices()
    if not all_hids:
        print("There's not any non system HID class device available")
    else:
        while True:
            print("Choose a device to monitor raw input reports:\n")
            print("0 => Exit")
            for index, device in enumerate(all_hids):
                device_name = unicode("{0.vendor_name} {0.product_name}" \
                        "(vID=0x{1:04x}, pID=0x{2:04x})"\
                        "".format(device, device.vendor_id, device.product_id))
                print("{0} => {1}".format(index+1, device_name))
            print("\n\tDevice ('0' to '%d', '0' to exit?) " \
                    "[press enter after number]:" % len(all_hids))
            index_option = raw_input()
            if index_option.isdigit() and int(index_option) <= len(all_hids):
                # invalid
                break
        int_option = int(index_option)
        if int_option:
            device = all_hids[int_option-1]
            try:
                device.open()

                #set custom raw data handler
                device.set_raw_data_handler(sample_handler)

                print("\nWaiting for data...\nPress any (system keyboard) key to stop...")
                while not kbhit() and device.is_plugged():
                    #just keep the device opened to receive events
                    for report in device.find_output_reports():
                        for target_usage in range(len(report)):
                            # found out target!
                           # report[target_usage] = 1 # yes, changing values is that easy
                            # at this point you could change different usages at a time...
                            # and finally send the prepared output report
                            report.send()
                            # now toggle back the signal
                            #report[target_usage] = 0
                           # report.send()
                            print(report)
                            sleep(0.2)


                    #sleep(1000)
                    pass
                return
            finally:
                device.close()

#
if __name__ == '__main__':
    # first be kind with local encodings
    import sys
    if sys.version_info >= (3,):
        # as is, don't handle unicodes
        unicode = str
        raw_input = input
    else:
        # allow to show encoded strings
        import codecs
        sys.stdout = codecs.getwriter('mbcs')(sys.stdout)

    target_vendor_id = 0x1234 # just an example, change it to the actual vendor_id
    target_usage = hid.get_full_usage_id(0xffa0, 0x02) # generic vendor page, usage_id = 2

    raw_test()

