__author__ = 'gabib3b'

import utils.numbersUtil as numbersUtils
import evenpaz.evenpaz1d as evenpazalg
import lastdiminisher.lastdiminisher1d as LastDiminisher
import utils.strategy as strategyUtil


def test_even_paz_simple():
    values = [1,2,3,4,5]
    noise = 0.1
    num_of_agents = 4
    #noise_values = numbersUtils.noisy_values_array(values, noise, None, num_of_agents)

    noise_values = [[10,20,5,10], [15,10,4,5], [5, 10, 10, 20], [4, 5, 15, 10]]

    even_paz_allocations = numbersUtils.values_to_allocations(noise_values)
    division_results = evenpazalg.even_paz_dividion(even_paz_allocations, 3)

    print(division_results)



test_even_paz_simple()