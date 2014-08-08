import changePriority
import TeensyInterface as ti

behaviours_config = 0

if behaviours_config == 0:
    from InteractiveCmd import InteractiveCmd as cmd
elif behaviours_config == 1:
    from Behaviours import HardcodedBehaviours_test as cmd
elif behaviours_config == 2:
    from Behaviours import HardcodedBehaviours as cmd
else:
    from InteractiveCmd import InteractiveCmd as cmd


packet_size_in = 64
packet_size_out = 64


if __name__ == '__main__':

    # change priority of the the Python process to HIGH
    changePriority.SetPriority(changePriority.Priorities.HIGH_PRIORITY_CLASS)

    # filter out the Teensy with vendor ID and product ID
    vendor_id = 0x16C0
    product_id = 0x0486

    # find all the Teensy
    serial_num_list = ti.find_teensy_serial_number(vendorID=vendor_id, productID=product_id)
    print("Number of Teensy devices found: " + str(len(serial_num_list)))

    # creating Teensy interface threads
    Teensy_thread_list = []
    Teensy_id = 0
    for serial_num in serial_num_list:
        print("Teensy " + str(Teensy_id) + " --- " + str(serial_num))
        Teensy_id += 1

        # create a new thread for communicating with
        try:
            Teensy_thread = ti.TeensyInterface(vendor_id, product_id, serial_num, unit_config='SIMPLIFIED_TEST_UNIT', print_to_term=False)
            Teensy_thread_list.append(Teensy_thread)

        except Exception as e:
            print(str(e))

    # interactive code
    behaviours = cmd(Teensy_thread_list)
    behaviours.run()

    # wait for each thread to terminate
    for t in Teensy_thread_list:
        t.join()

    print("All threads terminated")

