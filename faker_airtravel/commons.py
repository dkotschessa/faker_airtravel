from collections import OrderedDict

DATE_FORMAT = "%Y-%m-%d"
HOUR_FORMAT = "{:0d}:{:02d}"

def create_dict_weights(iterator, weights):
    return OrderedDict(
        (it, weight)
        for (it, weight) in zip(iterator, weights)
    )