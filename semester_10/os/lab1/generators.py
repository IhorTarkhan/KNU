import numpy as np


def int_normal_array_gen(size):
    return np.random.normal(size, (2 * size) / 6, size).astype(int)


def int_uniform_array_gen(size):
    return np.random.randint(0, 2 * size, size)


def int_asymptotic_array_gen(size):
    return np.random.exponential(2 * size / 10, size).astype(int)


def double_normal_array_gen(size):
    return np.random.normal(size, (2 * size) / 6, size)


def double_uniform_array_gen(size):
    return np.random.uniform(0, 2 * size, size)


def double_asymptotic_array_gen(size):
    return np.random.exponential(2 * size / 10, size)
