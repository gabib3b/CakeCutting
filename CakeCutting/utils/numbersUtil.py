

__author__ = 'gabib3b'
import random as rnd
import math
from evenpaz.allocation import Allocation
import utils.envInfluence as envInf
import sys
import random
import utils.calcOperations as calcOperations

def values_to_allocations(values):
    allocations = []
    for value in values:
        allocations.append(__allocate_from_number(value))

    return allocations


def __allocate_from_number(values):
    return Allocation(None, None, values)

def noisy_values(mean_values, noise_proportion, normalized_sum):

    aggregated_sum = 0
    values = [0] * len(mean_values)
    for i in range(len(mean_values)):
        noise = (2*rnd.random()-1)*noise_proportion
        newVal = mean_values[i]*(1+noise)
        newVal = max(0, newVal)
        aggregated_sum += newVal
        values[i] = newVal

    if aggregated_sum > 0 and normalized_sum is not None and normalized_sum > 0:
        normalization_factor = normalized_sum / aggregated_sum
        for i in range(len(values)):
            values[i] *= normalization_factor

    return values

def preference_values(mean_values, index_to_location_type, normalized_sum):

    current_agent_preferences = {}

    aggregated_sum = 0
    values = [0] * len(mean_values)
    for i in range(len(mean_values)):
        #noise = (2*rnd.random()-1)*noise_proportion
        factor = calc_preference_factor(i, index_to_location_type, current_agent_preferences)
        newVal = mean_values[i]*(factor)
        newVal = max(0, newVal)
        aggregated_sum += newVal
        values[i] = newVal

    if aggregated_sum > 0 and normalized_sum is not None and normalized_sum > 0:
        normalization_factor = normalized_sum / aggregated_sum
        for i in range(len(values)):
            values[i] *= normalization_factor

    return values


def calc_preference_factor(index, index_to_location_type, current_agent_preferences):

    if index in index_to_location_type:
        location_type = index_to_location_type[index].locationType()
        if location_type in current_agent_preferences:
            return current_agent_preferences[location_type]
        else:
         val = random_probability_for_preference()
         current_agent_preferences[location_type] = val
         return val
    else:
        return 1

def random_probability_for_preference():

    preferences_groups = envInf.PREFERENCES_PROBABILITY_GROUPS()
    from_index = sys.maxsize
    to_index = - sys.maxsize

    for preferences_group in preferences_groups:
        if preferences_group.start_index() < from_index:
            from_index = preferences_group.start_index()

        if preferences_group.end_index() > to_index:
            to_index = preferences_group.end_index()

    selected_index =  random.randint(from_index, to_index-1)

    selected_prob = None
    for preferences_group in preferences_groups:
         if preferences_group.start_index() <= selected_index and preferences_group.end_index() > selected_index:
             selected_prob =preferences_group
             break

    if selected_prob is None:
        raise Exception('selected_prob is None')

    from_val = selected_prob.min_value()
    to_val = selected_prob.max_value()
    selected_percentage = random.uniform(from_val, to_val)

    if selected_percentage < 0:
        return selected_percentage * -1
    else:
        return 1 + selected_percentage

def noisy_values_array(mean_values, noise_proportion, normalized_sum, num_of_agents):
    values = []
    for i in range(num_of_agents):
        values.append(noisy_values(mean_values, noise_proportion, normalized_sum))

    return values


def preferences_values_array(mean_values, index_location_type, normalized_sum, number_of_agents):
    values = []
    for i in range(number_of_agents):
        values.append(preference_values(mean_values, index_location_type, normalized_sum))

    return values

def env_influential_array(mean_values, noise_proportion, normalized_sum, num_of_agents):
    values = []
    for i in range(num_of_agents):
        values.append(env_influential_values(mean_values, noise_proportion, normalized_sum))

    return values

def special_places_indexes(mean_values):

    non_zero_indexes = []

    for index, value in  enumerate(mean_values):
        if value > 0:
            non_zero_indexes.append(index)

    number_of_special_places = int(non_zero_indexes / 20)



def env_influential_values(mean_values, noise_proportion, normalized_sum):

    aggregated_sum = 0
    values = [0] * len(mean_values)
    for i in range(len(mean_values)):
        noise = (2*rnd.random()-1)*noise_proportion
        newVal = mean_values[i]*(1+noise)
        newVal = max(0, newVal)
        aggregated_sum += newVal
        values[i] = newVal

    if aggregated_sum > 0 and normalized_sum is not None and normalized_sum > 0:
        normalization_factor = normalized_sum / aggregated_sum
        for i in range(len(values)):
            values[i] *= normalization_factor

    return values



#calc sum of the values array from index to index
# def sum_values(values, from_index, to_index):
#
#     if from_index < 0 or from_index > len(values):
#         raise RuntimeError('from_index not valid ' + from_index)
#
#     if to_index < 0 or to_index > len(values):
#         raise RuntimeError('to_index not valid ' + to_index)
#
#     if to_index < from_index:
#         raise RuntimeError('to_index not valid ' + to_index)
#
#     from_floor = int(math.floor(from_index))
#     from_fraction = (from_floor+1-from_index)
#     to_ceiling = int(math.ceil(to_index))
#     to_ceiling_removed_fraction = to_ceiling - to_index
#
#     calculated_sum = 0
#     calculated_sum += values[from_floor] * from_fraction
#
#     for index in range(from_floor + 1, to_ceiling):
#         calculated_sum += values[index]
#
#     calculated_sum -= values[to_ceiling - 1] * to_ceiling_removed_fraction
#
#     return calculated_sum

#return how many elemnts to take from from_index
def cut_index(values, target_sum, from_index, to_index):

    if from_index < 0 or from_index > len(values):
        raise RuntimeError('from_index not valid ' + from_index)

    if to_index < 0 or to_index > len(values):
        raise RuntimeError('to_index not valid ' + to_index)

    if to_index < from_index:
        raise RuntimeError('to_index not valid ' + to_index)

    from_floor = int(math.floor(from_index))
    from_fraction = from_floor + 1 - from_index
    value = values[from_floor]

    if value * from_fraction >= target_sum:
        return from_index + target_sum / value
    target_sum -= value * from_fraction

    for index in range(from_floor + 1, int(to_index)):
        value = values[index]
        if target_sum <= value:
            return index +target_sum/value
        target_sum -= value

    return len(values)


def relative_value(allocation):
    #allocation_sum = sum_values(allocation.values, allocation.fromIndex, allocation.toIndex)
    #total_sum = sum_values(allocation.values, 0, len(allocation.values))
    #return allocation_sum / total_sum
    return allocation.relative_value()

def egalitarianValue(allocations):
    #return relative_value(allocation)
   #    allocations.sort(key=operator.attrgetter('halfCut'))
   sorted(allocations, key= relative_value)
   return  relative_value(allocations[0])

def normalizedEgalitarianValue(allocations):
    return egalitarianValue(allocations) * len(allocations)

#return the sum of relative values of all agents.
def utilitarianValue(allocations):
    relative_sum = 0
    for allocation in allocations:
        relative_sum += relative_value(allocation)

    return  relative_sum


#how much the current values worth for each agent in fair division
def current_split_agent_value(values, from_index, to_index, number_of_agents):
    return calcOperations.sum_values(values, from_index, to_index) / number_of_agents


def current_split_allocation_value(allocation, from_index, to_index, number_of_agents):
    return allocation.values_sum(from_index, to_index)/ number_of_agents



def division_sum(values, from_index, to_index):
    return calcOperations.sum_values(values, from_index, to_index)


def set_allocations_grade(allocations):
    for allocation in allocations:
        set_allocation_grade(allocation)

def set_allocation_grade(allocation):
    allocation.grade = calcOperations.sum_values(allocation.values, allocation.fromIndex, allocation.toIndex)

























