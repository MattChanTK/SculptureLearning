import serial


class Interface:

    def __init__(self):

        self.port = None
        self.sensor_state = None


    def initSensor(self, com_port='COM9', baud_rate=9600):
        try:
            self.port = serial.Serial(com_port, baud_rate)
            print("Receiving data from " + self.port.name)
            self.port.flushOutput()
            return True
        except:
            print ("Cannot open " + com_port)
            return False


    def updateSensor(self):
        # read data stream from port
        x = self.port.readline()
        if x[-1] == '\n':
            x = x[0:-1]
        # tokenizing the string to sub-strings
        data = x.split(',')

        # converting them to numerical data
        try:
            self.sensor_state = [int(data[1]), int(data[2])]
       #     print(self.sensor_state)
        except:
            print(x)

        self.port.flushOutput()



    def closeSensor(self):
        print(self.port.name + " closed")
        self.port.close()


    def getSensorState(self):
        return self.sensor_state