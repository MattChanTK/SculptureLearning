from setup import*

class Expert:

    def __init__(self):

        self.error = []  # prediction error
        self.window = time_window
        self.smoothing = smoothing_parameter

    def predict(self):

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











