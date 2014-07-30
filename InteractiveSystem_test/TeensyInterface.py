import usb.core
import usb.util
import threading
import random
import struct

import SystemParameters as SysParam

class TeensyInterface(threading.Thread):

    packet_size_in = 64
    packet_size_out = 64

    def __init__(self, vendor_id, product_id, serial_num, print_to_term=False):

        # find our device
        dev = usb.core.find(idVendor=vendor_id, idProduct=product_id, serial_number=serial_num)
        # was it found?
        if dev is None:
            raise ValueError('Device not found')

        self.serial_number = serial_num

        # set the active configuration. With no arguments, the first
        # configuration will be the active one
        dev.set_configuration()

        # get an endpoint instance
        cfg = dev.get_active_configuration()

        interface_iter = usb.util.find_descriptor(cfg, find_all=True)
        interface = []
        for iter in interface_iter:
            interface.append(iter)
        self.intf = interface[0]

        # release device
        #usb.util.release_interface(dev, self.intf)
        # claiming device
        usb.util.claim_interface(dev, self.intf)

        # instantiate the system parameters
        self.param = SysParam.SystemParameters()

        # when True, param has been updated; set to back to False after sending a new message
        self.param_updated = False
        self.lock = threading.Lock()

        # start thread
        threading.Thread.__init__(self)
        self.daemon = False
        self.start()

        # print to terminal or not
        self.print_to_term = print_to_term

    def run(self):

        while True:

            self.lock.acquire()
            if self.param_updated:


                self.param_updated = False

                # compose the data
                out_msg, front_id, back_id = self.compose_msg()
                self.lock.release()

                # sending the data
                if self.print_to_term:
                    print("\n---Sent---")
                    self.print_data(out_msg, raw_dec=True)

                received_reply = False
                self.talk_to_Teensy(out_msg, timeout=0)

                # waiting for reply
                data = self.listen_to_Teensy(timeout=100, byte_num=TeensyInterface.packet_size_in)
                invalid_reply_counter = 0
                while data and received_reply is False:

                    # check if reply matches sent message
                    if data[0] == front_id and data[-1] == back_id:
                        if self.print_to_term:
                            print("---Received Reply---")
                            self.print_data(data, raw_dec=True)
                        received_reply = True
                    else:
                        if self.print_to_term:
                            print("......Received invalid reply......")
                            self.print_data(data, raw_dec=True)
                        # request another reply
                        data = self.listen_to_Teensy(timeout=100, byte_num=TeensyInterface.packet_size_in)
                    invalid_reply_counter += 1
                    if invalid_reply_counter > 5:
                        if 1: #self.print_to_term:
                            print( "......Number of invalid replies exceeded 5! Stopped trying......")
                            print("Sent:")
                            self.print_data(out_msg, raw_dec=True)
                            print("Received:")
                            self.print_data(data, raw_dec=True)
                        break
            else:
                self.lock.release()

    def compose_msg(self, rand_signature=True):

        content = self.param.compose_message_content()

        # check if content is in valid format
        if not isinstance(content, bytearray):
            raise TypeError("Content must be bytearray.")
        if len(content) is not 64:
            raise ValueError("Content must be 64 byte long.")


        # unique id for each message
        if rand_signature:
            front_id_dec = random.randint(0, 255)
            back_id_dec = random.randint(0, 255)
            front_id = struct.pack('c', chr(front_id_dec))
            back_id = struct.pack('c', chr(back_id_dec))
            content[0] = front_id
            content[-1] = back_id
        else:
            front_id_dec = 0
            back_id_dec = 0

        return content, front_id_dec, back_id_dec

    def listen_to_Teensy(self, timeout=100, byte_num=64):

        ep = usb.util.find_descriptor(
            self.intf,
            # match the first OUT endpoint
            custom_match = \
            lambda e: \
                usb.util.endpoint_direction(e.bEndpointAddress) == \
                usb.util.ENDPOINT_IN)

        assert ep is not None

        try:
            data = ep.read(byte_num, timeout)

        except usb.core.USBError:
            #print("Timeout! Couldn't read anything")
            data = None

        return data


    def talk_to_Teensy(self, out_msg, timeout=10):

        ep = usb.util.find_descriptor(
            self.intf,
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


    def print_data(self, data, raw_dec=False):
        if data:
            i = 0
            print("Serial Number: " + str(self.serial_number))
            print("Number of byte: " + str(len(data)))
            while i < len(data):
                if raw_dec:
                    char = int(data[i])
                else:
                    char = chr(data[i])
                print(char),
                i +=1

            print('\n')

