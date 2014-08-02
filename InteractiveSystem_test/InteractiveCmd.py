import threading
import queue


class InteractiveCmd(threading.Thread):

    def __init__(self):

        # command queue
        self.cmd_q = queue.Queue()

        # start thread
        threading.Thread.__init__(self)
        self.daemon = False
        self.start()


    def run(self):

        for i in range(4):
            cmd_obj = command_object(i)
            cmd_obj.add_param_change("param"+str(i), i*i)
            cmd_obj.add_param_change("param2"+str(i), i*4)
            self.get_command(cmd_obj)


       # self.get_command()

    def get_command(self, cmd=None):

        if isinstance(cmd, command_object):
            self.cmd_q.put(cmd)


        # prompt users for inputs
        elif cmd is None:
            cmd = input("Enter: [Teensy_ID] [param_type]:[param_value] (separated by space).\n" +
                        "To apply changes, enter '>>apply'.\n")

            param_cmd_list = cmd.split(" ")

            try:
                dev_id = int(param_cmd_list[0])
            except Exception as e:
                print(e)
                return -1

            cmd_obj = command_object(dev_id)

            for param_cmd in param_cmd_list[1:]:
                param = param_cmd.split(":")
                cmd_obj.add_param_change(param[0], param[1])

            self.cmd_q.put(cmd_obj)


    def send_command(self):
        pass


class command_object():

    def __init__(self, teensy_id):
        if not isinstance(teensy_id, int):
            raise TypeError("Teensy ID must be an integer!")

        self.teensy_id = teensy_id
        self.param_change = dict()

    def add_param_change(self, type, value):
        if isinstance(type, str):
            self.param_change[type] = value
        else:
            raise TypeError("'State type' must be a string!")

    def print(self):
        print(self.teensy_id, end=': ')
        for type, value in self.param_change.items():
            print('(', type, '-', value, ') ', end="")
        print('')



if __name__ == '__main__':

    t = InteractiveCmd()


    t.join()

    while not t.cmd_q.empty():
        t.cmd_q.get().print()


