import math

__author__ = 'gabib3b'


#calc sum of the values array from index to index
def sum_values(values, from_index, to_index):

    if from_index < 0 or from_index > len(values):
        raise RuntimeError('from_index not valid ' + from_index)

    if to_index < 0 or to_index > len(values):
        raise RuntimeError('to_index not valid ' + to_index)

    if to_index < from_index:
        raise RuntimeError('to_index not valid ' + to_index)

    from_floor = int(math.floor(from_index))
    from_fraction = (from_floor+1-from_index)
    to_ceiling = int(math.ceil(to_index))
    to_ceiling_removed_fraction = to_ceiling - to_index

    calculated_sum = 0
    calculated_sum += values[from_floor] * from_fraction

    for index in range(from_floor + 1, to_ceiling):
        calculated_sum += values[index]

    calculated_sum -= values[to_ceiling - 1] * to_ceiling_removed_fraction

    return calculated_sum