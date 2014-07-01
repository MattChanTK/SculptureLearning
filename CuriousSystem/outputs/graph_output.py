import csv
import matplotlib.pyplot as plt


time = '2014_07_01_14_39_28'
robot = 0

def plotData(time, robotID=0):

    filename_predictErr = time + '_prediction_error_' + str(robotID) + '.csv'
    filename_sensorHist = time + '_sensor_history_' + str(robotID) + '.csv'
    filename_actionHist = time + '_action_history_' + str(robotID) + '.csv'
    filename_stateHist = time + '_state_history_' + str(robotID) + '.csv'
    filename_lpHist = time + '_lp_history_' + str(robotID) + '.csv'

    figNum = 1


    # outputting prediction error graph
    try:
        with open(filename_predictErr, 'r') as csvfile:
            data = csv.reader(csvfile, delimiter=',') #import the data
            data = map(list, zip(*data))  #transpose the data
            data.pop()  # remove the empty row
            subplotNum = len(data)*100 + 11
            for row in data:
                row = [float(i) for i in row]
                fig = plt.figure(figNum)
                plt.subplot(subplotNum)

                subplotNum += 1
                plt.plot(row)

                plt.ylabel('Prediction Error')
                plt.xlabel('Time Step')
                plt.suptitle('Prediction Error Graph')
    except IOError:
        pass

    figNum += 1

     # outputting learning progress history graph
    try:
        with open(filename_lpHist, 'r') as csvfile:
            data = csv.reader(csvfile, delimiter=',') #import the data
            data = map(list, zip(*data))  #transpose the data
            data.pop()  # remove the empty row
            subplotNum = len(data)*100 + 11
            for row in data:
                row = [float(i) for i in row]
                fig = plt.figure(figNum)
                plt.subplot(subplotNum)
                subplotNum += 1
                plt.plot(row)
                plt.ylabel('Learning Progress')
                plt.xlabel('Time Step')
                plt.suptitle('Learning Progress Graph')
    except IOError:
        pass


    figNum += 1


    # outputting input history graph
    try:
        with open(filename_sensorHist, 'r') as csvfile:
            data = csv.reader(csvfile, delimiter=',') #import the data
            data = map(list, zip(*data))  #transpose the data
            data.pop()  # remove the empty row
            subplotNum = len(data)*100 + 11
            for row in data:
                row = [float(i) for i in row]
                fig = plt.figure(figNum)
                plt.subplot(subplotNum)
                subplotNum += 1
                plt.plot(row, '.')
                plt.ylabel('Input')
                plt.xlabel('Time Step')
                plt.suptitle('Input History Graph')

    except IOError:
        pass

    figNum += 1

    # outputting output history graph
    try:
        with open(filename_actionHist, 'r') as csvfile:
            data = csv.reader(csvfile, delimiter=',') #import the data
            data = map(list, zip(*data))  #transpose the data
            data.pop()  # remove the empty row
            subplotNum = len(data)*100 + 11
            for row in data:
                row = [float(i) for i in row]
                fig = plt.figure(figNum)
                plt.subplot(subplotNum)
                subplotNum += 1
                plt.plot(row, '.')
                plt.ylabel('Output')
                plt.xlabel('Time Step')
                plt.suptitle('Output History Graph')

    except IOError:
        pass
    figNum += 1

    # outputting state history graph
    try:
        with open(filename_stateHist, 'r') as csvfile:
            data = csv.reader(csvfile, delimiter=',') #import the data
            data = map(list, zip(*data))  #transpose the data
            data.pop()  # remove the empty row
            subplotNum = 200 + len(data)*10/2 + 1
            stateLabel = ['v', 'x', 'y', 'dir', 's1', 'm1', 's2_predict', 'm2']

            rowID = 0
            for row in data:

                row = [float(i) for i in row]
                fig = plt.figure(figNum)
                plt.subplot(subplotNum)
                subplotNum += 1
                plt.plot(row)
                plt.xlabel('Time Step')
                plt.suptitle('State History Graph')

                try:
                    plt.ylabel(stateLabel[rowID])
                except OverflowError:
                    plt.ylabel('state')
                rowID += 1
    except IOError:
        pass
    figNum += 1

    # outputting state-space diagram
    try:
        with open(filename_stateHist, 'r') as csvfile:
            data = csv.reader(csvfile, delimiter=',') #import the data
            data = map(list, zip(*data))  #transpose the data
            data.pop()  # remove the empty row

            plotState = [0, 4]
            stateLabel = ['v', 'x', 'y', 'dir', 's1', 'm1', 's2_predict', 'm2']

            xData = [float(i) for i in data[plotState[0]]]
            yData = [float(i) for i in data[plotState[1]]]

            plt.figure(figNum)
            plt.plot(xData, yData, '.')
            #for i in range(1, len(xData)):
            #    plt.arrow(xData[i-1], yData[i-1], xData[i]-xData[i-1],yData[i]-yData[i-1])

            plt.xlabel('state')
            plt.ylabel('state')
            try:
                plt.xlabel(stateLabel[plotState[0]])
                plt.ylabel(stateLabel[plotState[1]])
            except OverflowError:
                pass

            plt.suptitle('State Space Diagram')
    except IOError:
        pass
    figNum += 1

    # outputting Histogram
    try:
        with open(filename_stateHist, 'r') as csvfile:
            data = csv.reader(csvfile, delimiter=',') #import the data
            data = map(list, zip(*data))  #transpose the data
            data.pop()  # remove the empty row



            subplotNum = 200+ len(data)*10/2 + 1
            numBin = [100, 100, 100, 100, 100, 3, 100, 3]
            stateLabel = ['v', 'x', 'y', 'dir', 's1', 'm1', 's2_predict', 'm2']
            for plotState in range(0, len(data)):

                yData = [float(i) for i in data[plotState]]

                plt.figure(figNum)
                plt.subplot(subplotNum)
                subplotNum += 1
                plt.hist(yData, numBin[plotState])

                plt.xlabel('state')
                plt.ylabel('occurance')
                try:
                    plt.xlabel(stateLabel[plotState])
                except OverflowError:
                    pass

            plt.suptitle('State Space Diagram')
    except IOError:
        pass
    figNum += 1

    # # outputting action history graph
    # try:
    #     window = 300
    #     with open(filename_actionHist, 'r') as csvfile:
    #         data = csv.reader(csvfile, delimiter=',') #import the data
    #         data = map(list, zip(*data))  #transpose the data
    #         data.pop()  # remove the empty row
    #         subplotNum = len(data)*100 + 11
    #
    #         # convert action to percent action for each possible states
    #         bounds = []
    #         for row in data:
    #             row = [float(i) for i in row]
    #             bounds.append((min(row), max(row)))
    #
    #
    #         actData = []
    #         for row in data:
    #             row = [float(i) for i in row]
    #             bounds = (int(min(row)), int(max(row)))
    #
    #             actData_comp = []
    #             for type in range(bounds[0], bounds[1]+1):
    #
    #                 percentAct = []
    #                 for i in range(window, len(row)):
    #                     matched = 0
    #                     for act in row[i-window:i]:
    #                         if act == type:
    #                             matched += 1
    #                     percentAct.append(float(matched)/float(window))
    #                 actData_comp.append(tuple(percentAct))
    #             actData.append(tuple(actData_comp))
    #
    #         for comp in actData:
    #             fig = plt.figure(2)
    #             for type in comp:
    #                 plt.subplot(subplotNum)
    #                 plt.plot(type)
    #             subplotNum += 1
    #             plt.ylabel('Percent Action Taken (window='+str(window)+')')
    #             plt.xlabel('Time Step')
    #             plt.ylim([0, 1.0])
    #             plt.suptitle('Action Rate Graph')
    #             #plt.title('Sensor Signal ' + str(subplotNum - (len(data)*100+11)))
    #             #fig.subplots_adjust(hspace=1)
    # except IOError:
    #     pass
    plt.show()

plotData(time, robot)