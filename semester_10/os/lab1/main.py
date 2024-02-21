import copy
import datetime
import os
import tracemalloc

import numpy as np
import time

from generators import \
    int_normal_array_gen, \
    int_uniform_array_gen, \
    int_asymptotic_array_gen, \
    double_normal_array_gen, \
    double_uniform_array_gen, \
    double_asymptotic_array_gen
from sorters import bubble_sort, insertion_sort, merge_sort, quick_sort
from statistic import Comparator, Assigner

sorters = [merge_sort, quick_sort, bubble_sort, insertion_sort]
sizes = [10, 100, 1_000, 10_000, 100_000]
generators = [int_normal_array_gen,
              int_uniform_array_gen,
              int_asymptotic_array_gen,
              double_normal_array_gen,
              double_uniform_array_gen,
              double_asymptotic_array_gen]


class BenchmarkResult:
    def __init__(self, time_used, memory_used, compare_count, swap_count):
        self.time_used = time_used
        self.memory_used = memory_used
        self.swap_count = swap_count
        self.compare_count = compare_count

    def __str__(self):
        return f'BenchmarkResult(time_used={self.time_used}, memory_used={self.memory_used}, compare_count={self.compare_count}, swap_count={self.swap_count})'


def benchmark(array, sorter):
    tracemalloc.start()
    start_time = time.time()

    sorter(array)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    time_used = end_time - start_time

    return BenchmarkResult(time_used, peak, Comparator.reset(), Assigner.reset())


def average_benchmark(sorter, array_gen, size, iteration_count, skip_log=False):
    if not skip_log:
        print(f'{sorter.__name__}, {array_gen.__name__}, {size}')
        print(f'iterations: 0/{iteration_count}({datetime.datetime.now()}) (preparing...), ', end='')
    benchmark(copy.deepcopy(array_gen(size)), sorter)

    results = []
    for i in range(iteration_count):
        if not skip_log:
            print(f'{i + 1}/{iteration_count}({datetime.datetime.now()}), ', end='')
        results.append(benchmark(copy.deepcopy(array_gen(size)), sorter))

    return BenchmarkResult(
        time_used=np.mean([r.time_used for r in results]),
        memory_used=np.mean([r.memory_used for r in results]),
        swap_count=int(np.mean([r.swap_count for r in results])),
        compare_count=int(np.mean([r.compare_count for r in results])),
    )


def human_readable_benchmark():
    for sort in sorters:
        print(f'sort: {sort.__name__}')
        for gen in generators:
            for s in sizes:
                result = average_benchmark(sort, gen, s, 5)
                print(f'''
Result:
\tMemory used: {result.memory_used / 1024 :.2f} KB
\tTime used: {result.time_used:.2f} seconds
\tCompare used: {result.compare_count:,} times
\tSwap used: {result.swap_count:,} times''')
        print()


def report_benchmark():
    result = {}
    for sort in sorters:
        result[sort.__name__] = {}
        for gen in generators:
            result[sort.__name__][gen.__name__] = {}
            file = open(file_path, 'a')
            file.write(f'{sort.__name__}, {gen.__name__};')
            file.close()
            for s in sizes:
                r = average_benchmark(sort, gen, s, 3, True)
                result[sort.__name__][gen.__name__][s] = str(r)
                file = open(file_path, 'a')
                file.write(f'{r.memory_used / 1024 :.3f};{(r.compare_count + r.swap_count):,};{r.compare_count:,};{r.swap_count:,};{r.time_used:.3f};;')
                file.close()
            file = open(file_path, 'a')
            file.write('\n')
            file.close()

    file = open(file_path, 'a')
    file.write(str(result))
    file.close()


if __name__ == '__main__':
    file_path = 'log.csv'

    if os.path.exists(file_path):
        os.remove(file_path)
    # human_readable_benchmark()
    report_benchmark()
