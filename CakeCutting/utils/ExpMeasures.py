import csv
import utils.collectionsUtil as collectionsUtil

__author__ = 'gabib3b'


class ExpMeasures(object):

    def __init__(self, egalitarianGain, utilitarianGain, envy):
        self._egalitarianGain = egalitarianGain
        self._utilitarianGain = utilitarianGain
        self._envy = envy
        self._additional_fields = {}


    def addAdditionalData(self, key, value):
        self._additional_fields[key] = value


    def toCsv(self):

        return 'egalitarianGain,{0},utilitarianGain,{1},envy,{2}'.format(self._egalitarianGain, self._utilitarianGain, self._envy, collectionsUtil.convert_dict_to_str(self._additional_fields))


