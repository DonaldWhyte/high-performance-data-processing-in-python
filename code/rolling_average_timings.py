from statistics import mean
import time
from typing import List

import numpy as np


_INPUT_SIZE = 10000000
_WINDOW_SIZE = 30


def _main():
    _time_func(
        _rolling_average_py, list(range(_INPUT_SIZE)), _WINDOW_SIZE)
    _time_func(
        _rolling_average_np, np.arange(_INPUT_SIZE), _WINDOW_SIZE)
    _time_func(
        _rolling_average_vectorised, np.arange(_INPUT_SIZE), _WINDOW_SIZE)


def _time_func(func: callable, *args, **kwargs):
    start = time.time()
    func(*args, **kwargs)
    elapsed_time = time.time() - start
    print(f'{func} took {elapsed_time:.4f}s')


def _rolling_average_py(arr: List[int], n: int) -> np.ndarray:
    avg = np.zeros(len(arr) - n + 1)
    for i in range(len(avg)):
        avg[i] = mean(arr[i:i+n])
    return avg


def _rolling_average_np(arr: np.ndarray, n: int) -> np.ndarray:
    avg = np.zeros(len(arr) - n + 1)
    for i in range(len(avg)):
        avg[i] = arr[i:i+n].sum() / n
    return avg


def _rolling_average_vectorised(arr: np.ndarray, n: int) -> np.ndarray:
    ret = np.cumsum(arr, dtype=int)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


if __name__ == '__main__':
    _main()
