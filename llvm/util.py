from .common import c_object_p


def to_c_array(params):
    count = len(params)
    param_array = (c_object_p * count) ()
    for i in xrange(count):
        param_array[i] = params[i].from_param()
    return (count, param_array)
