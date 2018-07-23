from statistics import mean, stdev
from timeit import repeat


_NUM_TESTS = 10


def _main():
    sum2d_py = repeat(
        '''\
sum_array(a)
        ''',
        setup='''\
import numpy as np

def sum_array(arr):
    result = 0
    for i in range(len(arr)):
        result += arr[i]
    return result

a = np.arange(10000000)
        ''',
        number=1,
        repeat=_NUM_TESTS)

    sum2d_numba_inferred = repeat(
        '''\
sum_array(a)
        ''',
        setup='''\
from numba import jit
import numpy as np

@jit(nopython=True)
def sum_array(arr):
    result = 0
    for i in range(len(arr)):
        result += arr[i]
    return result

a = np.arange(10000000)

sum_array(a)
        ''',
        number=1,
        repeat=_NUM_TESTS)

    sum2d_numba_explicit = repeat(
        '''\
sum_array(a)
        ''',
        setup='''\
from numba import int64, jit
import numpy as np

@jit(int64(int64[:]), nopython=True)
def sum_array(arr):
    result = 0
    for i in range(len(arr)):
        result += arr[i]
    return result

a = np.arange(10000000)
        ''',
        number=1,
        repeat=_NUM_TESTS)

    sum2d_numpy = repeat(
        '''\
a.sum()
        ''',
        setup='''\
import numpy as np
a = np.arange(10000000)
        ''',
        number=1,
        repeat=_NUM_TESTS)

    _print_times('Summing numpy array (python)', sum2d_py)
    _print_times(
        'Summing numpy array (numba types inferred)', sum2d_numba_inferred)
    _print_times(
        'Summing numpy array (numba types explicit)', sum2d_numba_explicit)
    _print_times('Summing numpy array (numpy)', sum2d_numpy)


def _print_times(test_name, times):
    print(
        f'{test_name}: min={min(times):.4f}s, max={max(times):.4f}s, '
        f'avg={mean(times):.4f}s, stddev={stdev(times):.4f}s')


if __name__ == '__main__':
    _main()
