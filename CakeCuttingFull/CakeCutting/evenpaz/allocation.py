__author__ = 'gabib3b'

class Allocation(object):

    def __init__(self, from_index, to_index, values):

        if from_index is None:
            self.fromIndex = 0
        else:
            self.fromIndex = from_index

        if to_index is None:
            self.toIndex = len(values)
        else:
            self.toIndex = to_index

        self.values = values
        self.halfCut = -1
        self.grade = None


    def value(self):

        values = self.values

Allocation