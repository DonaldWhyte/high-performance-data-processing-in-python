import numpy as np
from numba import int64, jit


@jit(nopython=True)
def sum_array_inferred(arr):
    result = 0
    for i in range(len(arr)):
        result += arr[i]
    return result


@jit(int64(int64[:]), nopython=True)
def sum_array_explicit(arr):
    result = 0
    for i in range(len(arr)):
        result += arr[i]
    return result


def _main():
    print('DEDUCED TYPES BEFORE CALL')
    sum_array_inferred.inspect_types()

    print('Executing sum_array_inferred()')
    sum_array_inferred(np.arange(10000))

    print('DEDUCED TYPES AFTER CALL')
    sum_array_inferred.inspect_types()

    print("EXPLICIT TYPES")
    sum_array_explicit.inspect_types()


if __name__ == '__main__':
    _main()
