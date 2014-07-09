from sklearn.svm import SVR
from sklearn.cluster import KMeans
import numpy as np
import pylab as pl
import math
from mpl_toolkits.mplot3d import Axes3D

class Expert():


    def __init__(self):
        self.exemplar = dict()
        self.cluster_num = 1
        self.cluster = KMeans(n_clusters=1)
        self.partition = [dict()]*1
        self.model = [SVR(C=1.0, epsilon=0.2, gamma=0.5, kernel='linear')]*1

    def add_to_training_set(self, state_0, action_0, state_1):

        # add exemplar to main training set
        self.exemplar[tuple(state_0) + tuple(action_0)] = tuple(state_1)

        # reconstruct partitions

        self.cluster_num = int(max(1, (min(len(self.exemplar), math.floor(math.log(len(self.exemplar)+1)*1)))))

        # find clusters
        self.cluster = KMeans(n_clusters=self.cluster_num)
        self.cluster.fit(tuple(self.exemplar.keys()))
        self.partition = [None]*self.cluster_num
        self.model = [None]*self.cluster_num
        for i in range(self.cluster_num):
            self.partition[i] = dict()
            self.model[i] = SVR(C=1.0, epsilon=0.2, gamma=0.5, kernel='linear')

        # partition the training set based on the clusters
        for sa in tuple(self.exemplar.keys()):
            cluster_id = int(self.cluster.predict(sa)[0])
            self.partition[cluster_id][sa] = self.exemplar[sa]

        for i in range(len(self.partition)):
            print("Partition #" + str(i) + ": " + str(len(self.partition[i])))
        self.__train()


    def __train(self):

        for i in range(len(self.model)):
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

        sa = tuple(action_0) + tuple(state_0)
        model_id = 0

        # find the cluster that this data point belongs to
        try:
            model_id = self.cluster.predict(sa)[0]
        except:
            model_id = 0

        try:
            y = self.model[model_id].predict(sa)

        except AttributeError:
            y = [-1]

        return tuple(y)

    def plot_model(self, partition=0, show_plot=True):

        # plotting the data points
        fig = pl.figure(partition)
        ax = fig.add_subplot(111, projection='3d')
        for i in range(len(self.partition)):
            state = tuple(self.partition[i].keys())
            x_actual = []
            y_actual = []
            z_actual = []
            for x in state:
                x_actual.append(x[0])
                y_actual.append(x[1])
                z_actual.append(self.partition[i][x][0])
            x_actual = tuple(x_actual)
            y_actual = tuple(y_actual)
            z_actual = tuple(z_actual)

            if i == partition:
                colour = 'b'
            else:
                colour = 'k'

            ax.scatter(x_actual, y_actual, z_actual, color=colour)

        # plotting the model
        x = y = np.arange(0, 10, 0.05)
        X, Y = np.meshgrid(x, y)
        try:
            zs = np.array([self.model[partition].predict(tuple([x,y])) for x,y in zip(np.ravel(X), np.ravel(Y))])
            Z = zs.reshape(X.shape)
            ax.plot_surface(X, Y, Z, color='y', linewidth=0, cmap=pl.cm.coolwarm, antialiased=True)

        except AttributeError:
            print("Expert #" + str(partition) + " does not have a valid model.")

        ax.set_xlabel('State 0')
        ax.set_ylabel('Action 0')
        ax.set_zlabel('Predicted State 1')
        pl.title('Support Vector Regression Model (Partition #' + str(partition) + ")")

        if show_plot:
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