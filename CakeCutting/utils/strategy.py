from utils.IndexesToExchange import IndexesToExchange

__author__ = 'gabib3b'
from evenpaz.allocation import Allocation
import utils.calcOperations as calcOperations





def try_to_exchange_by_agents(allocations):

    index_to_change = None
    num_of_exchanges =0

    while True:

        for num in range(len(allocations)-1 ,0, -1):

            for i in range(num):
                first_allocation = allocations[i]
                second_allocation = allocations[i+1]


                first_allocation_value_on_second_allocation_range =  first_allocation.agent_value_for_indexes(second_allocation.fromIndex, second_allocation.toIndex)

                first_allocation_improvement = first_allocation_value_on_second_allocation_range - first_allocation.grade

                #case not improving for the first
                if first_allocation_improvement < 0:
                    continue

                second_allocation_value_on_first_allocation_range = second_allocation.agent_value_for_indexes(first_allocation.fromIndex, first_allocation.toIndex)

                second_allocation_improvement = second_allocation_value_on_first_allocation_range - second_allocation.grade

                if second_allocation_improvement >= 0 and (second_allocation_improvement > 0 or first_allocation_improvement > 0):
                   total_improvement = (second_allocation_improvement + first_allocation_improvement)
                   if index_to_change == None or (second_allocation_improvement + first_allocation_improvement) > index_to_change.improvement:
                       index_to_change = IndexesToExchange(i, i+1, total_improvement)


            if index_to_change is not None:
                from_index_i = allocations[i].fromIndex
                to_index_i = allocations[i].toIndex

                allocations[i].from_index=  allocations[i +1].fromIndex
                allocations[i].toIndex=  allocations[i +1].toIndex

                allocations[i+1].fromIndex = from_index_i
                allocations[i+1].toIndex= to_index_i
                num_of_exchanges += 1
                index_to_change = None

            else:#case no more changes return..
                return num_of_exchanges

    return 1
