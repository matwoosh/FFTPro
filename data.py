from enum import Enum
from math import sin, cos, sqrt, exp, floor, ceil
import numpy as np


class DerivativeType(Enum):
    central = 1
    backward = 2
    forward = 3


def function1(x, y):
    return sin(x)


def function2(x, y):
    return cos(x)


def function3(x, y):
    return x ** 2


def function4(x, y):
    return (x ** 3) - 9 * (x ** 2) + 25 * x - 17


def function5(x, y):
    return (x ** 4) - 3 * (x ** 2)


def function6(x, y):
    if x >= 0:
        return sqrt(x)
    else:
        return 0


def function7(x, y):
    return exp(x)


def function8(x, y):
    return abs(x)


def function9(x, y):
    return floor(x)


def function10(x,y):
    return 2 * x + ceil(x)


def function11(x,y):
    return floor(x) * x + ceil(x)

# list of functions_data in format ("name", function, arguments)
functions = [("sin(x)", function1, np.arange(0, 10, 0.01)),
             ("cos(x)", function2, np.arange(0, 10, 0.01)),
             ("x^2", function3, np.arange(0, 4, 0.01)),
             ("x^3 - 9x^2 + 25x - 17", function4, np.arange(0, 5, 0.01)),
             ("x^4 - 3x^2", function5, np.arange(0, 2, 0.01)),
             ("sqrt(x)", function6, np.arange(0, 10, 0.01)),  # something doesnt work here
             ("exp(x)", function7, np.arange(0, 10, 0.1)),
             ("|x|", function8, np.arange(-2, 2, 0.1)),
             ("floor(x)", function9, np.arange(-3, 3, 0.01)),
             ("2 * x + ceil(x)", function10, np.arange(-3, 3, 0.01)),
             ("floor(x) * x + ceil(x)", function11, np.arange(-3, 3, 0.01))]
