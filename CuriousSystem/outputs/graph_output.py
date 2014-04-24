import csv
import matplotlib.pyplot as plt
import sys


if len(sys.argv) > 1:

    filename_predictErr = str(sys.argv[1]) + '_prediction_error_0.csv'
    filename_actionRate = str(sys.argv[1]) + '_action_rate_0.csv'
    filename_stateHist = str(sys.argv[1]) + '_state_history_0.csv'
    filename_sensorHist = str(sys.argv[1]) + '_sensor_history.csv'
else:
    time = '2014_04_24_18_12_05'
    filename_predictErr = time + '_prediction_error_0.csv'
    filename_actionRate = time + '_action_rate_0.csv'
    filename_stateHist = time + '_state_history_0.csv'
    filename_sensorHist = time + '_sensor_history.csv'

# outputting prediction error graph
with open(filename_predictErr, 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=',') #import the data
    data = map(list, zip(*data))  #transpose the data
    data.pop()  # remove the empty row
    subplotNum = len(data)*100 + 11
    for row in data:
        row = [float(i) for i in row]
        fig = plt.figure(1)
        plt.subplot(subplotNum)
        subplotNum += 1
        plt.plot(row)
        plt.ylabel('Prediction Error')
        plt.xlabel('Time Step')


# outputting action history graph
window = 300
with open(filename_actionRate, 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=',') #import the data
    data = map(list, zip(*data))  #transpose the data
    data.pop()  # remove the empty row
    subplotNum = len(data)*100 + 11

    # convert action to percent action for each possible states
    bounds = []
    for row in data:
        row = [float(i) for i in row]
        bounds.append((min(row), max(row)))


    actData = []
    for row in data:
        row = [float(i) for i in row]
        bounds = (int(min(row)), int(max(row)))

        actData_comp = []
        for type in range(bounds[0], bounds[1]+1):

            percentAct = []
            for i in range(window, len(row)):
                matched = 0
                for act in row[i-window:i]:
                    if act == type:
                        matched += 1
                percentAct.append(float(matched)/float(window))
            actData_comp.append(tuple(percentAct))
        actData.append(tuple(actData_comp))

    for comp in actData:
        fig = plt.figure(2)
        for type in comp:
            plt.subplot(subplotNum)
            plt.plot(type)
        subplotNum += 1
        plt.ylabel('Percent Action Taken (window='+str(window)+')')
        plt.xlabel('Time Step')
        plt.ylim([0, 1.0])
        #plt.title('Sensor Signal ' + str(subplotNum - (len(data)*100+11)))
        #fig.subplots_adjust(hspace=1)

# outputting sensor history graph
with open(filename_sensorHist, 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=',') #import the data
    data = map(list, zip(*data))  #transpose the data
    data.pop()  # remove the empty row
    subplotNum = len(data)*100 + 11
    for row in data:
        row = [float(i) for i in row]
        fig = plt.figure(3)
        plt.subplot(subplotNum)
        subplotNum += 1
        plt.plot(row)
        plt.ylabel('Sensor Measurement (state)')
        plt.xlabel('Time Step')

# outputting state history graph
with open(filename_stateHist, 'r') as csvfile:
    data = csv.reader(csvfile, delimiter=',') #import the data
    data = map(list, zip(*data))  #transpose the data
    data.pop()  # remove the empty row
    subplotNum = len(data)*100 + 11
    for row in data:
        row = [float(i) for i in row]
        fig = plt.figure(4)
        plt.subplot(subplotNum)
        subplotNum += 1
        plt.plot(row)
        plt.ylabel('State')
        plt.xlabel('Time Step')
plt.show()
