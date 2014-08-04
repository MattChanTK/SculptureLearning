import threading
import queue
from time import clock

import TeensyInterface as ti


class InteractiveCmd():

    def __init__(self, Teensy_thread_list):

        # command queue
        self.cmd_q = queue.Queue()
        self.Teensy_thread_list = Teensy_thread_list


    def run(self):

        teensy_ids = range(len(self.Teensy_thread_list))
        led_period = [0]*len(self.Teensy_thread_list)
        indicator_led_on = [0]*len(self.Teensy_thread_list)

        while True:
        #for i in range(5):

            analog_0_samples = []
            if len(self.Teensy_thread_list) == 0:
                return

            for teensy_id in teensy_ids:

                # check if the thread is still alive
                if not self.Teensy_thread_list[teensy_id].is_alive():

                    self.Teensy_thread_list.pop(teensy_id)
                    led_period.pop(teensy_id)
                    indicator_led_on.pop(teensy_id)
                    teensy_ids = range(len(self.Teensy_thread_list))

                else:
                    cmd_obj = command_object(teensy_id)

                    cmd_obj.add_param_change('indicator_led_on',  int(indicator_led_on[teensy_id]))
                    cmd_obj.add_param_change('indicator_led_period', int(led_period[teensy_id])*25)
                    self.enter_command(cmd_obj)
                    start_time = clock()
                    self.send_commands()
                    sample, is_new_update = self.get_input_states(0, ('analog_0_state', ))
                    analog_0_samples.append(sample['analog_0_state'])
                    if is_new_update:
                        print(teensy_id, " - Echo time: ", clock() - start_time)
                        if analog_0_samples[teensy_id] > 850:
                            indicator_led_on[teensy_id] = 1
                        else:
                            indicator_led_on[teensy_id] = 0

                    # new blink period
                    led_period[teensy_id] += 0.002
                    led_period[teensy_id] %= 10


            print(analog_0_samples)


        # while True:
        #     self.enter_command()
        #     self.get_input_states(0, 'indicator_led_period')

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
            except Exception:
                print("Invalid change request!")
                return -1

            self.cmd_q.put(cmd_obj)

        print("Command Queue length: ", self.cmd_q.qsize())
        return 0

    def send_commands(self):
        while not self.cmd_q.empty():
            cmd_obj = self.cmd_q.get()
            t = threading.Thread(target=self.apply_change_request, args=(cmd_obj,))
            t.daemon = True
            t.start()

    def apply_change_request(self, cmd_obj):

        print("apply change request")
        if cmd_obj.teensy_id >= len(self.Teensy_thread_list):
            print("Teensy #" + str(cmd_obj.teensy_id) + " does not exist!")
            return -1
        self.Teensy_thread_list[cmd_obj.teensy_id].lock.acquire()
        self.Teensy_thread_list[cmd_obj.teensy_id].inputs_sampled_event.clear()

        try:
            #cmd_obj.print()
            for param_type, param_val in cmd_obj.change_request.items():
                self.Teensy_thread_list[cmd_obj.teensy_id].param.set_output_param(param_type, param_val)
            self.Teensy_thread_list[cmd_obj.teensy_id].param_updated_event.set()
            print(">>>>> sent command to Teensy #" + str(cmd_obj.teensy_id))
        except Exception as e:
            print(e)

        finally:
            self.Teensy_thread_list[cmd_obj.teensy_id].lock.release()

        return 0

    def get_input_states(self, teensy_id, input_types, timeout=0.005):

        if not isinstance(teensy_id, int):
            raise TypeError("Teensy ID must be integers!")
        if not isinstance(input_types, tuple):
            raise TypeError("'Input Types' must be inputted as tuple of strings!")

        # wait for sample update
        new_sample_received = self.Teensy_thread_list[teensy_id].inputs_sampled_event.wait(timeout=timeout)
        if new_sample_received:
            self.Teensy_thread_list[teensy_id].inputs_sampled_event.clear()

        requested_inputs = dict()
        for input_type in input_types:
            if not isinstance(input_type, str):
                raise TypeError("'Input type' must be a string!")

            try:
                requested_inputs[input_type] = self.Teensy_thread_list[teensy_id].param.get_input_state(input_type)
            except Exception as e:
                print(str(e))

        return requested_inputs, new_sample_received


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


