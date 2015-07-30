__author__ = 'gabib3b'

import matplotlib.pyplot as pyplot


"""
graph_values_presentation_value [min x, max x, min y, max y]
"""
def draw_graph(x_arr, y_arr, title, x_label, y_label, graph_values_presentation_value):

    #pyplot.plot(x_arr, y_arr, x_arr, y_arr * 2)

    pyplot.plot(x_arr, y_arr, x_arr, y_arr**2, x_arr, y_arr**3)
    pyplot.axis(graph_values_presentation_value)

    pyplot.title(title)
    pyplot.xlabel(x_label)
    pyplot.ylabel(y_label)


    pyplot.show()

