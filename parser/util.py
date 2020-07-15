from functools import reduce
from re import sub

# strip leading and trailing dots
def rlstrip_dot(string):
    return sub(r"^[\.]+|[\.\s]+$", "", string)


# helper function

# this function takes a number of functions and composes them
def composite_function(*func):

    def compose(f, g):
        return lambda x : f(g(x))

    return reduce(compose, func, lambda x : x)
