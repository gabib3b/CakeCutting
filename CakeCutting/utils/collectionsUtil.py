__author__ = 'gabib3b'


def convert_dict_to_str(data):
    result = ''
    for key in data:
        result += "{key} = {value}".format(key=key, value=data[key])
    return result
