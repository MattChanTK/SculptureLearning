import csv
import matplotlib.pyplot as plt
import sys

if len(sys.argv) > 1:
    filename = str(sys.argv[1])
else:
    filename = 'prediction_error_2014_03_24_03_32_59.csv'

with open(filename, 'rb') as csvfile:
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

    plt.show()
