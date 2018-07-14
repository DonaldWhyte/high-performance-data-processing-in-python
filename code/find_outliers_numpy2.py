import argparse
import csv
import datetime
import time
from typing import List, Optional, Tuple

import h5py
import numpy as np


_DIFFERENCE_RANGE = 1
_ROLLING_WINDOW = 14 * 6  # 7 days
_OUTLIER_STD_THRESHOLD = 9


def _main():
    args = _parse_args()
    _run(args.input, args.measurement, args.output)


def _run(input_fname: str, measurement: str, output_fname: Optional[str]):
    input_file = h5py.File(input_fname, mode='r')

    start_time = time.time()

    print('Determining range of each station time series')
    station_ids = input_file['station_usaf'][:1000000]
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
    measurements = input_file[measurement][:1000000]
    station_outliers = {
        station_ids[start]: compute_outliers(measurements[start:end],
                                             _ROLLING_WINDOW)
        for start, end in ranges_with_enough_data
    }

    elapsed_time = time.time() - start_time
    print(f'Computed outliers in {elapsed_time:.2f} seconds')

    if output_fname:
        print(f'Writing outliers to {output_fname}')
        timestamps = input_file['timestamp'][:1000000]
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
                        'value': measurements[outlier_index]
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


def series_ranges(station_ids: np.ndarray) -> List[Tuple[int, int]]:
    is_end_of_series = station_ids[:-1] != station_ids[1:]
    indices_where_stations_change = np.where(is_end_of_series == True)[0] + 1
    series_starts = np.concatenate((
        np.array([0]),
        indices_where_stations_change
    ))
    series_ends = np.concatenate((
        indices_where_stations_change,
        np.array([len(station_ids) - 1])
    ))
    return list(zip(series_starts, series_ends))


def compute_outliers(data: np.ndarray, n: int) -> np.ndarray:
    data = fill_forward(data)
    series_with_averages = data[n - 1:]
    avg = rolling_average(data, n)
    std = rolling_std(data, avg, n)
    return find_outliers(series_with_averages, avg, std)


def fill_forward(arr: np.ndarray) -> np.ndarray:
    mask = np.isnan(arr)
    indices_to_use = np.where(~mask, np.arange(mask.shape[0]), 0)
    np.maximum.accumulate(indices_to_use, axis=0, out=indices_to_use)
    return arr[indices_to_use]


def rolling_average(arr: np.ndarray, n: int) -> np.ndarray:
    ret = np.cumsum(arr, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def rolling_std(arr: np.ndarray, rolling_avg: np.ndarray, n: int) -> np.ndarray:
    variance = np.zeros(len(arr) - n + 1)
    assert len(variance) == len(rolling_avg)
    for i in range(len(variance)):
        variance[i] = np.sum(np.square(arr[i:i+n] - rolling_avg[i])) / n
    return np.sqrt(variance)


def find_outliers(series_with_avgs: np.ndarray,
                  rolling_avg: np.ndarray,
                  rolling_std: np.ndarray) -> np.ndarray:
    outlier_indices = np.where(
        np.absolute(series_with_avgs - rolling_avg) >
        (rolling_std * _OUTLIER_STD_THRESHOLD))
    return outlier_indices[0]


if __name__ == '__main__':
    _main()
