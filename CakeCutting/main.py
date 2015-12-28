import os
from utils.ExpMeasures import ExpMeasures
from utils.aggragationTYpe import AggregationType
from utils.algresult import AlgResult
from copy import deepcopy


__author__ = 'gabib3b'

import json
from evenpaz.allocation import Allocation
import utils.numbersUtil as numbersUtils
import evenpaz.evenpaz1d as evenpazalg
import lastdiminisher.lastdiminisher1d as LastDiminisher
import utils.strategy as strategyUtil
import utils.envInfluence as envEffect
import utils.expKey as ExpKey
import utils.additionalFields
import utils.experimentType as expType
import utils
import utils.envInfluence as envinfluence
import utils.cakepartitions as cakepartitionsUtil
from datetime import datetime




NOISE_PROPORTION = [0.2, 0.4, 0.6,0.8]
NUMBER_OF_AGENTS = [2,4,8,16,32,64,128,256,512]
#NUMBER_OF_AGENTS = [16, 32, 64,128,256,512]
DATA_FILE_NAME ='data/newzealand_forests_npv_4q.1d.json'
EXPERIMENTS_PER_CELL = 1



def run_ex_for_params(num_of_agents, noise, values):
    results_by_exp_type = {}

    for exp_type in expType.ExperimentType:
        results_by_exp_type[exp_type] =[]

    identical_values = numbersUtils.noisy_values_array(values, 0, None, num_of_agents)


    for exp in range(EXPERIMENTS_PER_CELL):
        noise_values = numbersUtils.noisy_values_array(values, noise, None, num_of_agents)

        allocations1  = numbersUtils.values_to_allocations(noise_values)
        identical_allocation_even_paz = numbersUtils.values_to_allocations(identical_values)

        #even paz..
        results_even_paz = calc_results_with_exchnages(evenpazalg.even_paz_dividion, expType.ExperimentType.even_paz, expType.ExperimentType.even_paz_exchange_jealous, allocations1,
                                                       num_of_agents, noise, None, identical_allocation_even_paz, expType.ExperimentType.even_paz_appraiser, results_by_exp_type)


        allocations2  = numbersUtils.values_to_allocations(noise_values)
        identical_allocation_last_diminisher = numbersUtils.values_to_allocations(identical_values)

        #last diminisher
        calc_results_with_exchnages(LastDiminisher.last_diminisher_allocation, expType.ExperimentType.last_diminisher, expType.ExperimentType.last_diminisher_exchange_jealous,
                                    allocations2, num_of_agents, noise, None, identical_allocation_last_diminisher, expType.ExperimentType.last_diminisher_appraiser, results_by_exp_type)

        #env influence
        index_to_location_type = envinfluence.index_to_location_type(values, envinfluence. LOCATION_TYPES())

        env_influence_values = numbersUtils.preferences_values_array(values, index_to_location_type, None,  num_of_agents)

        #even paz
        even_paz_env_allocations = numbersUtils.values_to_allocations(env_influence_values)
        calc_results_with_exchnages(evenpazalg.even_paz_dividion, expType.ExperimentType.even_paz_env_influence, expType.ExperimentType.even_paz_env_influence_exchange,
                                    even_paz_env_allocations, num_of_agents, 0, None, None, None, results_by_exp_type)


        #last diminisher
        last_diminisher_env_allocations = numbersUtils.values_to_allocations(env_influence_values)
        calc_results_with_exchnages(LastDiminisher.last_diminisher_allocation, expType.ExperimentType.last_diminisher_env_influence, expType.ExperimentType.last_diminisher_env_influence_exchange,
                                    last_diminisher_env_allocations, num_of_agents, 0, None, None, None, results_by_exp_type)

        #fraud agent

        for i in range(num_of_agents):

           identical_allocation_last_diminisher_i = numbersUtils.values_to_allocations(identical_values)

           allocations_even_paz_fraud  = numbersUtils.values_to_allocations(noise_values)

           calc_results_with_exchnages(evenpazalg.even_paz_dividion, expType.ExperimentType.even_paz_fraud_agenct_index,
                                        expType.ExperimentType.even_paz_fraud_agent_index_with_exchange, allocations_even_paz_fraud, num_of_agents, noise, i,
                                        identical_allocation_last_diminisher_i, expType.ExperimentType.even_paz_fraud_identical, results_by_exp_type)

           allocations_last_diminisher_fraud = numbersUtils.values_to_allocations(noise_values)

           calc_results_with_exchnages(LastDiminisher.last_diminisher_allocation, expType.ExperimentType.last_diminisher_fraud_agent_index,
                                       expType.ExperimentType.last_diminisher_fraud_agent_index_with_exchange, allocations_last_diminisher_fraud, num_of_agents, noise, i,
                                       identical_allocation_last_diminisher_i, expType.ExperimentType.last_diminisher_fraud_identical, results_by_exp_type)



    #calc mid

    for type, results in results_by_exp_type.items():
        for result in results:
            #todo: calc average from same type of alg..
            pass

    return results_by_exp_type



def run_2(num_of_agents, noise, values):

     print('start calculating agencts-{0} , noise-{1},  {2}'.format(num_of_agents, noise, datetime.utcnow()))

     identical_values = numbersUtils.values_to_allocations(numbersUtils.noisy_values_array(values, 0, None, num_of_agents))

     noise_values = numbersUtils.values_to_allocations(numbersUtils.noisy_values_array(values, noise, None, num_of_agents))

     index_to_location_type = envinfluence.index_to_location_type(values, envinfluence. LOCATION_TYPES())

     env_influence_values = numbersUtils.values_to_allocations(numbersUtils.preferences_values_array(values, index_to_location_type, None,  num_of_agents))

     ldResults = calc_single_row(num_of_agents, noise, deepcopy(noise_values), deepcopy(identical_values), deepcopy(env_influence_values), LastDiminisher.last_diminisher_allocation)

     print('ldResults calculated {0}'.format(datetime.utcnow()))

     evenPazResults = calc_single_row(num_of_agents, noise, deepcopy(noise_values), deepcopy(identical_values), deepcopy(env_influence_values), evenpazalg.even_paz_dividion)

     print('evenPazResults calculated {0}'.format(datetime.utcnow()))

     return  evenPazResults,ldResults





def calc_single_row(num_of_agents, noise, values, identical_values, env_influence_values, main_alg_method):


    #main alg
    main_alg_division = main_alg_method(deepcopy(values), None)
    main_alg_measures = cakepartitionsUtil.alg_division_to_measures(main_alg_division)


    #main alg with exchange
    #todo: clone the division
    exchange_main_alg_division = deepcopy(main_alg_division)
    numbersUtils.set_allocations_grade(exchange_main_alg_division)
    main_alg_num_of_changes = strategyUtil.try_to_exchange_by_agents(exchange_main_alg_division)
    exchange_main_alg_measures = cakepartitionsUtil.alg_division_to_measures(exchange_main_alg_division)
    exchange_main_alg_measures.addAdditionalData('num_of_changes', main_alg_num_of_changes)

    #identical values
    identical_values_main_alg_division = main_alg_method(identical_values, None)
    identical_alg_measures = cakepartitionsUtil.alg_division_to_measures(identical_values_main_alg_division)


    #identical with exchange
     #todo: clone the division
    exchange_identical__main_alg_division = deepcopy(identical_values_main_alg_division)
    numbersUtils.set_allocations_grade(exchange_identical__main_alg_division)
    main_with_identical__alg_num_of_changes = strategyUtil.try_to_exchange_by_agents(exchange_identical__main_alg_division)
    exchange_identical_alg_measures = cakepartitionsUtil.alg_division_to_measures(exchange_identical__main_alg_division)
    exchange_identical_alg_measures.addAdditionalData('num_of_changes', main_with_identical__alg_num_of_changes)

    #env influence
    main_alg_division_env_influence = main_alg_method(env_influence_values, None)
    influence_alg_measures = cakepartitionsUtil.alg_division_to_measures(main_alg_division_env_influence)

    #env influence after change
    exchange_identicalenv_influence_main_alg_division = deepcopy(main_alg_division_env_influence)
    numbersUtils.set_allocations_grade(exchange_identicalenv_influence_main_alg_division)
    main_with_env_influence_alg_num_of_changes = strategyUtil.try_to_exchange_by_agents(exchange_identicalenv_influence_main_alg_division)
    exchange_influence_alg_measures = cakepartitionsUtil.alg_division_to_measures(exchange_identicalenv_influence_main_alg_division)
    exchange_influence_alg_measures.addAdditionalData('num_of_changes', main_with_env_influence_alg_num_of_changes)


    fraud_agent_index_to_fraud_division = {}
    fraud_agent_index_to_measures = {}

    for agent_index in range(num_of_agents):
        fraud_main_alg_division = main_alg_method(deepcopy(values), agent_index)
        fraud_agent_index_to_fraud_division[agent_index] = fraud_main_alg_division
        fraud_agent_index_to_measures[agent_index] = cakepartitionsUtil.alg_division_to_measures(fraud_main_alg_division, False)


    return AlgResult(num_of_agents, noise, main_alg_measures, identical_alg_measures, influence_alg_measures,
                     fraud_agent_index_to_measures, exchange_main_alg_measures, exchange_identical_alg_measures, exchange_influence_alg_measures)



def calc_results_with_exchnages(first_alg_method, first_exp_type, second_exp_type, values, num_of_agents, noise, fraud_agent_index, identical_values, identical_exp_type, results_by_exp_type):

     res = {}
     division = first_alg_method(values, fraud_agent_index)
     additional1 = {}
     if fraud_agent_index is not None:
        additional1[utils.additionalFields.fraud_agenct_index()] = fraud_agent_index



     if identical_values is not None:
        identical_values_division = first_alg_method(identical_values, fraud_agent_index)
        results_by_exp_type[identical_exp_type].append(ExpKey.ExpKey(identical_exp_type, num_of_agents, 0, identical_values_division, additional1))


     results_by_exp_type[first_exp_type].append(ExpKey.ExpKey(first_exp_type, num_of_agents, noise, division, additional1))
     numbersUtils.set_allocations_grade(division)
     num_of_changes = strategyUtil.try_to_exchange_by_agents(division)

     additional = {}
     additional[utils.additionalFields.numberOfExchanges()] = num_of_changes

     if fraud_agent_index is not None:
        additional[utils.additionalFields.fraud_agenct_index()] = fraud_agent_index

     #res[second_exp_type] = ExpKey.ExpKey(second_exp_type, num_of_agents, noise, division, additional)
     results_by_exp_type[second_exp_type].append(ExpKey.ExpKey(second_exp_type, num_of_agents, noise, division, additional))

     return res


def mean_values():


    with open(DATA_FILE_NAME) as json_file:
       origin_values = json.load(json_file)

    return origin_values


def calculate_results(aggregationType):

    values = mean_values()

    dirPath = 'results/{0}'.format(datetime.utcnow().strftime("%Y_%m_%d_%M_%S"))

    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

    if aggregationType == AggregationType.NUmberOfAgents:

        for agent_number in NUMBER_OF_AGENTS:
            print(agent_number)
            evenPazResultsFileName =  "{0}/evenpaz-agents-{1}.dat".format(dirPath, agent_number)
            ldResultsFileName =  "{0}//ld-agents-{1}.dat".format(dirPath, agent_number)
            print('even paz result file {0}'.format(evenPazResultsFileName))
            print('last diminisher result file {0}'.format(ldResultsFileName))

            evenPazWriter = open(evenPazResultsFileName,'w')
            ldWriter = open(ldResultsFileName,'w')

            for noise in NOISE_PROPORTION:
                evenPazResults , ldREsults = run_2(agent_number, noise, values)
                evenPazResultsStr = evenPazResults.toCsv()
                evenPazWriter.write(evenPazResultsStr + '\n')

                ldResultsStr = ldREsults.toCsv()
                ldWriter.write(ldResultsStr + '\n')


            evenPazWriter.close()
            ldWriter.close()

    elif aggregationType == AggregationType.Noise:

         for noise in NOISE_PROPORTION:
            evenPazResultsFileName =  "{0}/evenpaz-noise-{1}.dat".format(dirPath, noise)
            ldResultsFileName =  "{0}/ld-noise-{1}.dat".format(dirPath, noise)
            evenPazWriter = open(evenPazResultsFileName,'w')
            ldWriter = open(ldResultsFileName,'w')


            for agent_number in NUMBER_OF_AGENTS:
                evenPazResults , ldREsults = run_2(agent_number, noise, values)
                evenPazResultsStr = evenPazResults.toCsv()
                evenPazWriter.write(evenPazResultsStr + '\n')

                ldResultsStr = ldREsults.toCsv()
                ldWriter.write(ldResultsStr + '\n')

            evenPazWriter.close()
            ldWriter.close()

    else:
        raise Exception("Aggregation Type is not supported.. "+ aggregationType)



if __name__ == '__main__':
    calculate_results(AggregationType.NUmberOfAgents)
    print('completed..')



