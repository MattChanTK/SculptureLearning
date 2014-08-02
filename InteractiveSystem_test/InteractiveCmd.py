import threading
import queue

import TeensyInterface as ti


class InteractiveCmd(threading.Thread):

    def __init__(self, Teensy_thread_list):

        # command queue
        self.cmd_q = queue.Queue()
        self.Teensy_thread_list = Teensy_thread_list

        # start thread
        threading.Thread.__init__(self)
        self.daemon = False
        self.start()


    def run(self):

        # for i in range(1):
        #     try:
        #         cmd_obj = command_object(0)
        #         cmd_obj.add_param_change('indicator_led_on',  1)
        #         cmd_obj.add_param_change('indicator_led_period',  500)
        #         self.enter_command(cmd_obj)
        #     except Exception as e:
        #         print(e)
        while True:
            self.enter_command()

    def enter_command(self, cmd=None):

        if isinstance(cmd, command_object):
            self.cmd_q.put(cmd)

        # prompt users for inputs
        elif cmd is None:
            cmd = input("Enter--> [Teensy_ID] [param_type]:[param_value] (separated by space).\n" +
                        "To apply changes, enter '>>apply'.\n")

            # tokenize the command
            param_cmd_list = cmd.split(" ")

            # check if it's the "apply" command
            try:
                applying_cmd = str(param_cmd_list[0])
                if applying_cmd == ">>apply":
                    self.send_commands()
                    return 1
            except Exception as e:
                print(e)
                return -1

            # extract the Teensy ID
            try:
                dev_id = int(param_cmd_list[0])
            except ValueError:
                 print("Teensy ID must be integer!")
                 return -1

            # create a command object
            cmd_obj = command_object(dev_id)

            # extracts the parameters change requests
            try:
                for param_cmd in param_cmd_list[1:]:
                    param = param_cmd.split(":")
                    cmd_obj.add_param_change(param[0], param[1])
            except Exception as e:
                print("Invalid change request! --- ", e, )
                return -1

            self.cmd_q.put(cmd_obj)

        print("Command Queue length: ", self.cmd_q.qsize())
        return 0

    def send_commands(self):
        while not self.cmd_q.empty():
            cmd_obj = self.cmd_q.get()
            threading.Thread(target=self.apply_change_request(cmd_obj))


    def apply_change_request(self, cmd_obj):

        self.Teensy_thread_list[cmd_obj.teensy_id].lock.acquire()
        self.Teensy_thread_list[cmd_obj.teensy_id].inputs_sampled_event.clear()

        try:
            #cmd_obj.print()
            for param_type, param_val in cmd_obj.change_request.items():
                self.Teensy_thread_list[cmd_obj.teensy_id].param.set_output_param(param_type, param_val)
            self.Teensy_thread_list[cmd_obj.teensy_id].param_updated_event.set()
        except Exception as e:
            print(e)
        finally:
            self.Teensy_thread_list[cmd_obj.teensy_id].lock.release()
        print(">>>>> sent command to Teensy #" + str(cmd_obj.teensy_id))


class command_object():

    def __init__(self, teensy_id):
        if not isinstance(teensy_id, int):
            raise TypeError("Teensy ID must be an integer!")

        self.teensy_id = teensy_id
        self.change_request = dict()

    def add_param_change(self, type, value):
        if isinstance(type, str):
            self.change_request[type] = value
        else:
            raise TypeError("'State type' must be a string!")

    def print(self):
        print(self.teensy_id, end=': ')
        for type, value in self.change_request.items():
            print('(', type, '-', value, ') ', end="")
        print('')



if __name__ == '__main__':

    t = InteractiveCmd()


    t.join()

    while not t.cmd_q.empty():
        t.cmd_q.get().print()


