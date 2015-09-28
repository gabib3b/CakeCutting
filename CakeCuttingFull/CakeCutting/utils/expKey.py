__author__ = 'gabib3b'

class ExpKey(object):

    def __init__(self, alg_name, number_of_agents, _noise, division, additional_values_map):
        self.__alg_name = alg_name
        self._number_of_agents = number_of_agents
        self._noise = _noise
        self._division = division
        self._additional_values_map = additional_values_map


    def algName(self):
        return self.__alg_name

    def numberOfAgents(self):
        return self._number_of_agents

    def noise(self):
        return self._noise

    def division(self):
        return self._division

    def additionalValuesMap(self):
        return self._additional_values_map
