from collections import OrderedDict


def create_dict_weights(iterator, weights):
    return OrderedDict(
        (it, weight)
        for (it, weight) in zip(iterator, weights)
    )