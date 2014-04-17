import csv
import matplotlib.pyplot as plt
import sys
import copy

if len(sys.argv) > 1:
    #filename = str(sys.argv[1])
    filename_predictErr = str(sys.argv[1]) + '_prediction_error.csv'
    filename_action = str(sys.argv[1]) + '_action_error.csv'
else:
    #filename = '2014_03_24_13_36_16_prediction_error.csv'
    time = '2014_04_17_09_18_41'
    filename_predictErr = time +'_prediction_error.csv'
    filename_action = time + '_action_error.csv'

# outputting prediction error graph
with open(filename_predictErr, 'rb') as csvfile:
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
        #plt.title('Sensor Signal ' + str(subplotNum - (len(data)*100+11)))
        #fig.subplots_adjust(hspace=1)

'''
# outputting action history graph
window = 300
with open(filename_action, 'rb') as csvfile:
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
        for type in range(bounds[0], bounds[1]):

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
        plt.ylim([0, 0.50])
        #plt.title('Sensor Signal ' + str(subplotNum - (len(data)*100+11)))
        #fig.subplots_adjust(hspace=1)
'''

plt.show()
