from setup import*
from sklearn import svm
import Sensor

class Expert:

    def __init__(self):

        self.error = []  # prediction error
        self.window = time_window
        self.smoothing = smoothing_parameter

        # knowledge by training
        self.model = []  # set of trained knowledge
        # weight for action selection
        self.Q = []

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

        # print len(y_train[0])
        # train for each output dimension
        for i in range(0, numYDim):
            try:
                self.model[i].fit(x_train, y_train[i])
            except ValueError:
                temp_x_train = copy.copy(x_train)
                temp_y_train = copy.copy(y_train[i])
                x_append = [x + 0.1 for x in temp_x_train[0]]
                y_append = temp_y_train[0] + 0.1
                temp_x_train.append(x_append)
                temp_y_train.append(y_append)
                self.model[i].fit(temp_x_train, temp_y_train)

    def predict(self, sensor, motor):

        prediction = []
        sm = sensor.getParam() + motor.getParam()

        for i in range(0, len(self.model)):
            try:
                p = self.model[i].predict(sm)[0]
            except AttributeError:  # if can't make a prediction
                p = (sensor.getParam())[i] # just use the input value as best guess

            prediction.append(copy.copy(p))

        return Sensor.Sensor(prediction, simple=sensor.isSimple())

    def addPredictError(self, s_actual, s_prediction):

        if len(self.error)+1 > (self.smoothing+self.window):
            # forget oldest one if full
            self.error.pop(0)

        actual = s_actual.getParam()
        prediction = s_prediction.getParam()

        error = [0]*len(actual)
        for i in range(0, len(error)):
            error[i] = actual[i] - prediction[i]
        self.error.append(error)
        return error

    def calcLearningProgress(self):

        numParam = len(self.error[0])
        mean_err_0 = [0]*numParam
        mean_err = [0]*numParam
        numError = len(self.error)

        for i in range(0, numParam):
            for j in range(numError - self.smoothing, numError):
                mean_err[i] += self.error[j][i]

        for i in range(0, numParam):
            for j in range(0, numError - self.window):
                mean_err_0[i] += self.error[j][i]

        learnProgress = [0]*numParam
        for i in range(0, numParam):
            mean_err[i] /= self.smoothing
            mean_err_0[i] /= self.smoothing
            learnProgress[i] = mean_err_0[i] - mean_err[i]
        return learnProgress












