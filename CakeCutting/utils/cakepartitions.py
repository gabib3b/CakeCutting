import math
from utils.ExpMeasures import ExpMeasures

__author__ = 'gabib3b'

from evenpaz.allocation import Allocation
from utils import numbersUtil as Numbersutil
from utils import calcOperations


def largest_envy(allocations):
    largest_envy_value = -1
    for allocation in allocations:
        largest_envy_value = max(largest_envy_of_agent(allocation, allocations), largest_envy_value)

    return largest_envy_value

def largest_envy_of_agent(allocation_to_compare, allocations):
    max_envy_found = 0
    for allocation in allocations:
        max_envy_found = max(envy_of_agent(allocation_to_compare, allocation), max_envy_found)

    return  max_envy_found


def agent_value(values, from_index, to_index):
    return calcOperations.sum_values(values, from_index, to_index)

def agent_value_for_indexes(allocation, from_index, to_index):
    return allocation.agent_value_for_indexes(from_index, to_index)


def envy_of_agent(allocation, other_allocation):
    envious_value = agent_value_for_indexes(allocation, allocation.fromIndex, allocation.toIndex)
    envied_value = agent_value_for_indexes(allocation, other_allocation.fromIndex, other_allocation.toIndex)

    if envious_value >= envied_value:
        return 0
    else:
        gap =envied_value - envious_value
        env = gap/envious_value
        return env

def alg_division_to_measures(division, validate = True):

    egalitarianGain = Numbersutil.normalizedEgalitarianValue(division) -1

    if  validate and  egalitarianGain <- 0.001:
        raise  Exception ("In proportional division, normalized egalitarian gain must be at least 0; got "+egalitarianGain)

    utilitarianGain = Numbersutil.utilitarianValue(division) -1

    if  validate and  utilitarianGain <- 0.001:
        raise  Exception ("In proportional division, utilitarian gain must be at least 0; got "+utilitarianGain)

    envy = largest_envy(division)

    return ExpMeasures(egalitarianGain, utilitarianGain, envy)



