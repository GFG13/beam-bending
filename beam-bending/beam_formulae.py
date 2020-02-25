## beam formulae
import numpy as np


def circle_area(diameter):
    area = np.pi * (diameter / 2) ** 2
    return area


def square_area(length, width):
    area = length * width
    return area


def p_result(distributed_load, x):
    p_res = distributed_load * x
    return p_res


def moment(f, x_arm):
    m = f * x_arm
    return m


def stress(moment_sum, r):
    sig = (moment_sum * r) / (1 / 4 * np.pi * r ** 4)
    return sig
