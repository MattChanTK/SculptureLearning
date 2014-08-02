import threading
import sys


class InteractiveCmd(threading.Thread):

    def __init__(self):

        # start thread
        threading.Thread.__init__(self)
        self.daemon = False
        self.start()

    def run(self):
        self.__prompt()
        pass

    def __prompt(self):

        cmd = input("Enter action as (param_type, param_value). To apply changes, type '-apply'.\n")
        print(cmd)

if __name__ == '__main__':

    t = InteractiveCmd()