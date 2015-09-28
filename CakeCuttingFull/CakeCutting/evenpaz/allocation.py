__author__ = 'gabib3b'
import utils.calcOperations

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
        self.relative_values = {}
        self.sum_values = {}
        self.halfCutValues = {}



    def value(self):

        values = self.values

    def relative_value(self):
        relative_value_index = '{0}_{1}'.format(self.fromIndex, self.toIndex)

        if relative_value_index not in self.relative_values:
            allocation_sum = self.values_sum(self.fromIndex, self.toIndex)
            total_sum = self.values_sum(0, len(self.values))
            self.relative_values[relative_value_index] = allocation_sum / total_sum

        return self.relative_values[relative_value_index]



    def values_sum(self, from_index, to_index):
        sum_values_index = '{0}_{1}'.format(from_index, to_index)
        if sum_values_index not in self.sum_values:
            self.sum_values[sum_values_index] = utils.calcOperations.sum_values(self.values, from_index, to_index)

        return self.sum_values[sum_values_index]


    def agent_value_for_indexes(self, from_index, to_index):
        return self.values_sum(from_index, to_index)

    def halfCut(self, proportional_value, fraud_agent_index, allocations):
        pass




Allocation