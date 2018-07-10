import math
import time
from typing import List, Optional

import numpy as np


_INPUT_SIZE = 1000000


def _main():
    py_list = [
        math.nan if i % 1000 == 0 else float(i)
        for i in range(_INPUT_SIZE)
    ]
    np_array = np.array(py_list)

    _time_func(_fill_forward_py, py_list)
    _time_func(_fill_forward_np, np_array)
    _time_func(_fill_forward_vectorised, np_array)


def _time_func(func: callable, *args, **kwargs):
    start = time.time()
    func(*args, **kwargs)
    elapsed_time = time.time() - start
    print(f'{func} took {elapsed_time:.4f}s')


def _fill_forward_py(arr: List[Optional[float]]):
    if math.isnan(arr[0]):
        last_value =
    last_value = arr[0]
    for i in range(1, len(arr)):
        if math.isnan(arr[i]):
            arr[i] = arr[i - 1]
        else:
            last_value = arr[i]


def _fill_forward_np(arr: np.ndarray):
    for i in range(1, len(arr)):
        if math.isnan(arr[i]):
            arr[i] = arr[i - 1]


def _fill_forward_vectorised(arr: np.ndarray) -> np.ndarray:
    mask = np.isnan(arr)
    indices_to_use = np.where(~mask, np.arange(mask.shape[0]), 0)
    np.maximum.accumulate(indices_to_use, axis=0, out=indices_to_use)
    return arr[indices_to_use]


if __name__ == '__main__':
    _main()
