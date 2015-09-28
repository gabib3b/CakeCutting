__author__ = 'gabib3b'

class ExpResult(object):

    def __init__(self, num_of_agents, noise, egalitarianGain, utilitarianGain, envy, egalitarianGainIPWDA, utilitarianGainIPWDA, envyIPWDA):
        self._num_of_agents = num_of_agents
        self._noise = noise
        self._egalitarianGain = egalitarianGain
        self._utilitarianGain = utilitarianGain
        self._envy = envy
        self._egalitarianGainIPWDA = egalitarianGainIPWDA
        self._utilitarianGainIPWDA = utilitarianGainIPWDA
        self._envyIPWDA = envyIPWDA

    def numberOfAgents(self):
        return  self._num_of_agents

    def noise(self):
        return self._noise

    def egalitarianGain(self):
        return self._egalitarianGain

    def utilitarianGain(self):
        return self._utilitarianGain

    def envy(self):
        return self._envy

    def egalitarianGainIPWDA(self):
        return self._egalitarianGainIPWDA

    def utilitarianGainIPWDA(self):
        return self._utilitarianGainIPWDA

    def envyIPWDA(self):
        return self._envyIPWDA
















