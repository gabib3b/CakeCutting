__author__ = 'gabib3b'


class AlgResult(object):


    def __init__(self, numOfAgents, noiseProportion, mainAlgResult, resultForIPWDA,
                  envResult, fraudAgentIndexToResult, mainAlgAfterChange, resultForIPWDAAfterChange, envResultAfterChange):

        self._numberOfAgents = numOfAgents
        self._noiseProportion = noiseProportion
        self._mainAlgResult = mainAlgResult
        self._resultForIPWDA = resultForIPWDA
        self._envResult = envResult
        self._fraudAgentIndexToResult = fraudAgentIndexToResult
        self._mainAlgAfterChange = mainAlgAfterChange
        self._resultForIPWDAAfterChange = resultForIPWDAAfterChange
        self._envResultAfterChange = envResultAfterChange

    def toCsv(self):

        fraudCsv = ''
        for key in  self._fraudAgentIndexToResult:
            fraudCsv +='agenctINdex_'+str(key) + ',' + self._fraudAgentIndexToResult[key].toCsv() +','

        fraudCsv[0:len(fraudCsv)-1]

        return 'NUmberOfAgents,{0},noise,{1},mainAlgResult,{2},resultForIPWDA,{3},envResult,{4},fraudAgentIndexToResult,{5},mainAlgAfterChange,{6},resultForIPWDAAfterChange,{7},envResultAfterChange,{8}'.format(self._numberOfAgents, self._noiseProportion, self._mainAlgResult.toCsv(),
                                                             self._resultForIPWDA.toCsv(),self._envResult.toCsv(), fraudCsv,
                                                             self._mainAlgAfterChange.toCsv(), self._resultForIPWDAAfterChange.toCsv(), self._envResultAfterChange.toCsv())


