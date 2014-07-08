
class Expert():

    def __init__(self):
        self.exemplar = dict()

    def add_to_training_set(self, state_0, action_0, state_1):
        self.exemplar[tuple(state_0) + tuple(action_0)] = tuple(state_1)
        print self.exemplar

    @staticmethod
    def test():
        expert = Expert()
        expert.add_to_training_set([0],[1], [2])
        expert.add_to_training_set([4],[5], [6])

#Expert.test()