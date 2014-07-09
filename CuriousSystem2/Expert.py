from sklearn.svm import SVR
from sklearn.cluster import KMeans
import numpy as np
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D

class Expert():

    cluster_num = 1
    def __init__(self):
        self.exemplar = dict()

        self.cluster = KMeans(n_clusters=Expert.cluster_num)
        self.partition = [dict()]*Expert.cluster_num
        self.model = [SVR(C=1.0, epsilon=0.2, gamma=0.5, kernel='rbf')]*Expert.cluster_num

    def add_to_training_set(self, state_0, action_0, state_1):

        # add exemplar to main training set
        self.exemplar[tuple(state_0) + tuple(action_0)] = tuple(state_1)

        # find clusters
        self.cluster.fit(tuple(self.exemplar.keys()))

        # partition the training set based on the clusters
        for sa in tuple(self.exemplar.keys()):
            cluster_id = self.cluster.predict(sa)[0]
            self.partition[cluster_id][sa] = self.exemplar[sa]
        self.__train()


    def __train(self):

        for i in range (len(self.model)):
            X = tuple(self.partition[i].keys())
            y = []
            for x in X:
                y.append(self.partition[i][x][0])
            y = tuple(y)

            if len(self.partition[i]) > 1:
                try:
                    self.model[i].fit(X, y)
                except ValueError:
                    pass

    def predict(self, state_0, action_0):
        try:
            y = self.model[0].predict(tuple(action_0) + tuple(state_0))

        except AttributeError:
            y = -1

        return y

    def plot_model(self):

        # plotting the data points
        state = tuple(self.exemplar.keys())
        x_actual = []
        y_actual = []
        z_actual = []
        for x in state:
            x_actual.append(x[0])
            y_actual.append(x[1])
            z_actual.append(self.exemplar[x][0])
        x_actual = tuple(x_actual)
        y_actual = tuple(y_actual)
        z_actual = tuple(z_actual)


        fig = pl.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x_actual, y_actual, z_actual, color='k')
        pl.hold('on')


        # plotting the model
        x = y = np.arange(0, 10, 0.05)
        X, Y = np.meshgrid(x, y)
        try:
            zs = np.array([self.model[0].predict(tuple([x,y])) for x,y in zip(np.ravel(X), np.ravel(Y))])
            Z = zs.reshape(X.shape)
        except AttributeError:
            print("Expert does not have a valid model.")


        ax.plot_surface(X, Y, Z, color='y', linewidth=0, cmap=pl.cm.coolwarm, antialiased=True)
        ax.set_xlabel('State 0')
        ax.set_ylabel('Action 0')
        ax.set_zlabel('Predicted State 1')
        pl.title('Support Vector Regression Model')
        pl.show()



    @staticmethod
    def test():
        expert = Expert()

        for i in range(10):
            expert.add_to_training_set([i], [i+1], [-i])
        #expert.add_to_training_set([4], [5], [6])
        for i in range(10):
            print expert.predict([i], [i+1])
#Expert.test()