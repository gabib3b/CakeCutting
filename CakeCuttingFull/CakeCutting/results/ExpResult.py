__author__ = 'gabib3b'

class ExpResult(object):

    def __init__(self, alg_name, x_name, y_name, points):

        self._alg_name = alg_name
        self._x_name = x_name
        self._y_name = y_name
        self._points = points


    def algName(self):
        return self._alg_name

    def xName(self):
        return self._x_name

    def yName(self):
        return self._y_name

    def points(self):
        return self._points

