__author__ = 'gabib3b'

import evenpaz.evenpaz1d as evenpazutils
import utils.numbersUtil as numbersUtils

def last_diminisher_dividion(values):
    allocations = evenpazutils.proportional_division_even_paz(values)


def allocate_by_last_diminisher(allocations, next_agent_index, division_from_index, division_to_index, winning_agent_index):

    if next_agent_index > len(allocations) -1:
        allocations.pop(winning_agent_index)

        if len(allocations) > 0:
            #todo: set the indexes from the selected..
            return allocate_by_last_diminisher(allocations, 0, 0, len(allocations[0].values) -1, None)

    else:
        return 1


def last_diminisher_allocation(allocations, fraudAgentIndex = None):

    allocated_agents = []
    from_index = 0

    while len(allocations) > 0:
        number_of_agents = len(allocations)
        if number_of_agents == 1:
            allocated_agents.append(allocations[0])
            break

        to_index = len(allocations[0].values)
        selected_agent_index = -1
        selected_allocation = None
        for index, allocation in enumerate(allocations):

            #fraud will calculate at the end..
            if fraudAgentIndex  is not None and index == fraudAgentIndex:
                continue

            agent_allocation = check_division_for_agent(allocation, from_index, to_index, number_of_agents)
            if agent_allocation is not None:
                if selected_allocation is not None:
                    selected_allocation.toIndex = len(selected_allocation.values)

                selected_agent_index = index
                selected_allocation = agent_allocation
                to_index = selected_allocation.toIndex
                #from_index = to_index


        if selected_allocation is None:
            raise Exception('selected allocation was NULL')


        if fraudAgentIndex is not None:
            fraud_agent_allocation = check_division_for_agent(allocations[fraudAgentIndex], from_index, to_index, number_of_agents)
        else:
            fraud_agent_allocation = None

        if fraud_agent_allocation is not None:
            #fraud agent would
            fraud_agent_allocation.toIndex = selected_allocation.toIndex - 0.000001
            selected_allocation = fraud_agent_allocation
            selected_agent_index = fraudAgentIndex



        allocated_agents.append(selected_allocation)
        allocations.pop(selected_agent_index)
        from_index = to_index

        if fraudAgentIndex is not None and selected_agent_index != fraudAgentIndex:
            if selected_agent_index < fraudAgentIndex:
                fraudAgentIndex -= 1
        elif fraudAgentIndex is not None and fraudAgentIndex == selected_agent_index:
            fraudAgentIndex = None

        #since the piece was taken by the selected agent
        #we can check the value on smaller territory..
        for allocation in allocations:
            allocation.fromIndex = from_index
            allocation.toIndex = len(allocation.values)

    return allocated_agents



def check_division_for_agent(allocation, from_index, to_index, number_of_agents):
    agent_fair_value = numbersUtils.current_split_allocation_value(allocation, allocation.fromIndex, allocation.toIndex, number_of_agents)
    current_allocation_value = allocation.values_sum(from_index, to_index)
    #numbersUtils.division_sum(allocation.values, from_index, to_index)

    if agent_fair_value >= current_allocation_value:
        return None
    else:
      return divide_smaller_for_agent(allocation, from_index, to_index, number_of_agents)



def  divide_smaller_for_agent(allocation, from_index, to_index, number_of_agents):
    agent_fair_value = numbersUtils.current_split_allocation_value(allocation, allocation.fromIndex, allocation.toIndex, number_of_agents)
    agent_to_index = numbersUtils.cut_index(allocation.values, agent_fair_value, from_index,  allocation.toIndex)

    allocation.fromIndex = from_index
    allocation.toIndex = agent_to_index

    return allocation















