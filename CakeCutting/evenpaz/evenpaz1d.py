from evenpaz.allocation import Allocation
from utils import numbersUtil as Numbersutil
import operator

__author__ = 'gabib3b'

import utils.calcOperations as calcOperations

# run Evenpaz on 1 dimention input..



def even_paz_dividion(allocations, fraudAgentIndex = None):
    number_of_agents = len(allocations)

    if number_of_agents == 1:
        return allocations

    if number_of_agents % 2 == 0:
        num_of_agents_in_first_partition = int(number_of_agents / 2)
    else:
        num_of_agents_in_first_partition = int((number_of_agents + 1) / 2)

    proportion_of__first_partition = num_of_agents_in_first_partition / float(number_of_agents)


    for index in range(len(allocations)):
        allocations_with_cut = None
        if index > 0 and  fraudAgentIndex is not None and fraudAgentIndex == index:
            allocations_with_cut = allocations[0: index +1]
        allocations[index].halfCut = calc_half_cut(allocations[index], proportion_of__first_partition, fraudAgentIndex, allocations_with_cut)



    cut_location = cut_index(allocations[:])

    first_part_allocations, second_part_allocations = split_by_cut_location(allocations, cut_location, True)

    first_part_fraud_agent_index = None;
    second_part_fraud_agent_index = None

    if fraudAgentIndex is not None:
        for index, second_allocation in  enumerate(second_part_allocations):
            if second_allocation is allocations[fraudAgentIndex]:
                second_part_fraud_agent_index = index #fraudAgentIndex -len(first_part_allocations)
                first_part_fraud_agent_index = None
                break

        if second_part_fraud_agent_index is None:
            for index, first_allocation in enumerate(first_part_allocations):
                if(first_allocation is allocations[fraudAgentIndex]):
                    second_part_fraud_agent_index = None
                    first_part_fraud_agent_index = index
                    break

        if second_part_fraud_agent_index is None and first_part_fraud_agent_index is None:
            raise Exception('fraud agent was not found ' + fraudAgentIndex)


    first_part_results = even_paz_dividion(first_part_allocations, first_part_fraud_agent_index)

    second_part_results = even_paz_dividion(second_part_allocations, second_part_fraud_agent_index)

    first_part_results.extend(second_part_results)

    return first_part_results

def cut_index(allocations):

    number_of_agents = len(allocations)

    if number_of_agents == 0:
        raise Exception("number_of_agents can not be zero..")

    if number_of_agents == 1:
       return 0

    if number_of_agents % 2 == 0:
        num_of_agents_in_first_partition = int(number_of_agents / 2)
    else:
        num_of_agents_in_first_partition = int((number_of_agents + 1) / 2)

    allocations.sort(key=operator.attrgetter('halfCut'))

    end_of_first_part = allocations[num_of_agents_in_first_partition-1].halfCut;
    start_of_second_part = allocations[num_of_agents_in_first_partition].halfCut;
    cut_location = (end_of_first_part + start_of_second_part)/2

    return cut_location

def split_by_cut_location(allocations, cut_location, assignIndexes):

    number_of_agents = len(allocations)

    if number_of_agents % 2 == 0:
        num_of_agents_in_first_partition = int(number_of_agents / 2)
    else:
        num_of_agents_in_first_partition = int((number_of_agents + 1) / 2)

    first_part_allocations = []
    second_part_allocations = []
    tmp_equal_half_cut_allocation = []
    for allocation in allocations:
        if allocation.halfCut < cut_location:
            first_part_allocations.append(allocation)
            if assignIndexes:
                allocation.toIndex = cut_location
        elif allocation.halfCut > cut_location:
            second_part_allocations.append(allocation)
            if assignIndexes:
                allocation.fromIndex = cut_location
        else:
            tmp_equal_half_cut_allocation.append(allocation)

    for allocation in tmp_equal_half_cut_allocation:
        if len(first_part_allocations) < num_of_agents_in_first_partition:
            first_part_allocations.append(allocation)
            if assignIndexes:
                allocation.toIndex = cut_location
        else:
            second_part_allocations.append(allocation)
            if assignIndexes:
                allocation.fromIndex = cut_location

    return first_part_allocations, second_part_allocations


def calc_half_cut(allocation, proportional_value, fraud_agent_index, allocations):

    calculated_sum = allocation.values_sum(allocation.fromIndex, allocation.toIndex)
    target_sum = proportional_value * calculated_sum
    host_cut_index = Numbersutil.cut_index(allocation.values, target_sum, allocation.fromIndex, allocation.toIndex)

    if allocations is not None:

        allocation.halfCut = host_cut_index
        current_cut_location = cut_index(allocations[:])
        first_part, second_part = split_by_cut_location(allocations, current_cut_location, False)

        first_part.sort(key=operator.attrgetter('halfCut'))
        second_part.sort(key=operator.attrgetter('halfCut'))

        is_fraud_in_first_part = False

        for first_allocation in first_part:
            if first_allocation is allocations[fraud_agent_index]:
                is_fraud_in_first_part = True
                break

        first_index_right_item = first_part[len(first_part)-1]
        second_index_left_item = second_part[0]
        #todo: remove halfcut from fraud index..
        if is_fraud_in_first_part:
            return second_index_left_item.halfCut - 0.000001
        else:
            return first_index_right_item.halfCut + 0.000001

    else:
        return host_cut_index




