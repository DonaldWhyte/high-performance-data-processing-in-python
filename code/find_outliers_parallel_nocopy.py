import argparse
import csv
import datetime
from multiprocessing import cpu_count
import time
from typing import List, Optional, Tuple

import h5py
from joblib import delayed, Parallel
from numba import float64, int64, jit, typeof
import numpy as np


_DIFFERENCE_RANGE = 1
_ROLLING_WINDOW = 14 * 6  # 7 days
_OUTLIER_STD_THRESHOLD = 9


def read_only_array(dtype):
    x = np.empty((0,), dtype=dtype)
    x.flags.writeable = False
    return typeof(x)


def _main():
    args = _parse_args()
    _run(args.input, args.measurement, args.output)


def _run(input_fname: str, measurement: str, output_fname: Optional[str]):
    # Load input data before starting timer. We're only interested in measuring
    # computation time, not disk IO or memory speed.
    input_file = h5py.File(input_fname, mode='r')
    station_ids = input_file['station_usaf'][:]

    # Write the measurement data to an memmap'd file. This file is shared
    # across all worker subprocesses.
    from tempfile import NamedTemporaryFile
    tmpfile = NamedTemporaryFile()
    data = np.memmap(
        tmpfile.name,
        dtype=np.float64,
        shape=(len(input_file[measurement]),),
        mode='w+')
    data[:] = input_file[measurement][:]
    del data  # flushes contents to disk

    start_time = time.time()

    print('Determining range of each station time series')
    ranges = series_ranges(station_ids)
    print(f'Found time series for {len(ranges)} ranges')

    print('Removing time series that don\'t have enough data')
    ranges_with_enough_data = [
        (start, end) for start, end in ranges
        if end - start >= (_DIFFERENCE_RANGE + _ROLLING_WINDOW + 1)
    ]
    print(
        'Kept', len(ranges_with_enough_data), '/', len(ranges),
        'station time series')

    print('Computing outliers')

    processor = Parallel(n_jobs=cpu_count())
    results = processor(
        delayed(compute_outliers)(tmpfile.name, start, end, _ROLLING_WINDOW)
        for start, end in ranges_with_enough_data)

    station_outliers = {
        station_ids[start_index]: result
        for (start_index, _), result in zip(ranges_with_enough_data, results)
    }

    elapsed_time = time.time() - start_time
    print(f'Computed outliers in {elapsed_time:.2f} seconds')

    if output_fname:
        print(f'Writing outliers to {output_fname}')
        timestamps = input_file['timestamp']
        with open(output_fname, 'wt') as out_file:
            writer = csv.DictWriter(
                out_file,
                fieldnames=('station_usaf', 'timestamp', 'value'))
            for station_id in sorted(station_outliers.keys()):
                writer.writerows([
                    {
                        'station_usaf': station_id,
                        'timestamp': datetime.datetime.utcfromtimestamp(
                            timestamps[outlier_index]),
                        'value': all_data[outlier_index]
                    }
                    for outlier_index in station_outliers[station_id]
                ])


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='path to input HDF5 file containing data to find outliers in')
    parser.add_argument(
        '-m', '--measurement',
        required=True,
        help='measurement to find outliers in')
    parser.add_argument(
        '-o', '--output',
        help='name of output CSV file that contains outliers')
    return parser.parse_args()


@jit(int64[:, :](int64[:]), nopython=True)
def series_ranges(station_ids):
    is_end_of_series = station_ids[:-1] != station_ids[1:]
    indices_where_stations_change = np.where(is_end_of_series == 1)[0] + 1
    series_starts = np.concatenate((
        np.array([0]),
        indices_where_stations_change
    ))
    series_ends = np.concatenate((
        indices_where_stations_change,
        np.array([len(station_ids) - 1])
    ))
    return np.column_stack((series_starts, series_ends))


def compute_outliers(memmap_fname, start, end, n):
    data = fill_forward(
        np.memmap(memmap_fname, dtype=np.float64, mode='r')[start:end])
    series_with_averages = data[n - 1:]
    avg = rolling_average(data, n)
    std = rolling_std(data, avg, n)
    return find_outliers(series_with_averages, avg, std)


def fill_forward(arr):
    mask = np.isnan(arr)
    indices_to_use = np.where(~mask, np.arange(mask.shape[0]), np.array([0]))
    np.maximum.accumulate(indices_to_use, axis=0, out=indices_to_use)
    return arr[indices_to_use]


@jit(float64[:](read_only_array(np.float64), int64), nopython=True)
def rolling_average(arr, n):
    ret = np.cumsum(arr)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


@jit(float64[:](read_only_array(np.float64), float64[:], int64), nopython=True)
def rolling_std(arr, rolling_avg, n):
    variance = np.zeros(len(arr) - n + 1)
    assert len(variance) == len(rolling_avg)
    for i in range(len(variance)):
        variance[i] = np.sum(np.square(arr[i:i+n] - rolling_avg[i])) / n
    return np.sqrt(variance)


@jit(int64[:](read_only_array(np.float64), float64[:], float64[:]), nopython=True)
def find_outliers(series_with_avgs: np.ndarray,
                  rolling_avg: np.ndarray,
                  rolling_std: np.ndarray) -> np.ndarray:
    outlier_indices = np.where(
        np.absolute(series_with_avgs - rolling_avg) >
        (rolling_std * _OUTLIER_STD_THRESHOLD))
    return outlier_indices[0]


if __name__ == '__main__':
    _main()
