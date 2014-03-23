from setup import*
from sklearn import svm
import Sensor
import copy

class Expert:

    def __init__(self):

        self.error = []  # prediction error
        self.window = time_window
        self.smoothing = smoothing_parameter

        # knowledge by training
        self.model = []  # set of trained knowledge

    def train(self, exemplars):

        # get the number of dimensions
        numYDim, yIndex = exemplars[0].getNumOutputParams()
        numXDim = exemplars[0].getNumParams() - numYDim

        if not self.model:
            #for each output dimension
            for i in range(0, numYDim):
                # using Support Vector Regression (rbf)
                self.model.append(svm.SVR())


        # constructing the training set
        x_train = []
        y_train = []
        for i in range(0, numYDim):
            y_train.append([0]*len(exemplars))
        # for each exemplar
        for expId in range(0, len(exemplars)):
            x_train.append(exemplars[expId].getSM())
            s2 = exemplars[expId].getS2()
            for i in range(0, len(s2)):
                y_train[i][expId] = s2[i]

        # train for each output dimension
        for i in range(0, numYDim):
            try:
                self.model[i].fit(x_train, y_train[i])
            except ValueError:
                temp_x_train = copy.copy(x_train)
                temp_y_train = copy.copy(y_train[i])
                temp_x_train.append([0]*len(x_train[0]))
                temp_y_train.append(0)
                self.model[i].fit(temp_x_train, temp_y_train)



    def predict(self, sensor, motor):

        prediction = []
        sm = sensor.getParam() + motor.getParam()

        for i in range(0, len(self.model)):
            try:
                p = self.model[i].predict(sm)[0]
            except AttributeError:  # if can't make a prediction
                p = (sensor.getParam())[i] # just use the input value as best guess

            prediction.append(p)

        return Sensor.Sensor(prediction)


    def addPredictError(self, actual, prediction):

        if len(self.error)+1 > (self.smoothing+self.time_window):
            # forget oldest one if full
            self.error.pop(0)

        error = actual - prediction
        self.error.append(error)

    def calcLearningProgress(self):

        numParam = len(self.error[0])
        mean_err_0 = [0]*numParam
        mean_err = [0]*numParam
        numError = len(self.error)

        for i in range(0, numParam):
            for j in range(numError - self.smoothing, numError):
                mean_err[i] += self.error[j][i]

        for i in range(0, numParam):
            for j in range(0, numError - self.smoothing):
                mean_err_0[i] += self.error[j][i]

        return mean_err_0 - mean_err











