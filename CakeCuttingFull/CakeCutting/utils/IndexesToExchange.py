__author__ = 'gabib3b'

class IndexesToExchange(object):
    def __init__(self, first_index, second_index, improvement):
        self.first_index = first_index
        self.second_index = second_index
        self.improvement = improvement

    def __eq__(self, other):
        if other == None:
            return False

        return self.first_index == other.first_index and self.second_index == other.second_index

    def __hash__(self):
        return hash(self.first_index, self.second_index)


