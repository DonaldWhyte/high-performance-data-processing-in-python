import argparse
import csv
import datetime
import h5py
from multiprocessing import Pool
from numba import jit
import numpy as np
import time


_DIFFERENCE_RANGE = 1
_ROLLING_WINDOW = 14 * 6  # 7 days
_OUTLIER_STD_THRESHOLD = 9


def _main():
    args = _parse_args()
    _run(args.input, args.measurement, args.output)


def _run(input_fname: str, measurement: str, output_fname: str):
    input_file = h5py.File(input_fname, mode='r')

    start_time = time.time()

    print('Determining range of each station time series')
    station_ids = input_file['station_usaf']
    is_end_of_series = station_ids[:-1] != station_ids[1:]
    series_ends = np.where(is_end_of_series == True)[0]
    series_starts = np.concatenate([np.array([0]), series_ends + 1])
    series_ranges = list(zip(series_starts, series_ends))
    print(f'Found time series for {len(series_ranges)} ranges')

    print('Removing time series that don\'t have enough data')
    ranges_with_enough_data = [
        (start, end) for start, end in series_ranges
        if end - start >= (_DIFFERENCE_RANGE + _ROLLING_WINDOW + 1)
    ]
    print(
        'Kept', len(ranges_with_enough_data), '/', len(series_ranges),
        'station time series')

    print('Computing outliers')
    measurements = input_file[measurement]
    station_outliers = {
        station_ids[start]: _compute_outliers(measurements[start:end],
                                              _ROLLING_WINDOW)
        for start, end in ranges_with_enough_data
    }

    elapsed_time = time.time() - start_time
    print(f'Computed outliers in {elapsed_time:.2f} seconds')

    print(f'Writing outliers to {output_fname}')
    timestamps = input_file['timestamp']
    with open(output_fname, 'wt') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=('station_usaf', 'timestamp', 'value'))
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
        required=True,
        help='name of output CSV file that contains outliers')
    return parser.parse_args()


def _compute_outliers(data: np.array, n: int) -> np.array:
    data = _fill_forward(data)

    avg = _rolling_average(data, n)
    std = _rolling_std(data, avg, n)
    series_with_std = data[n - 1:]

    outlier_indices = np.where(
        np.absolute(series_with_std - avg) > (std * _OUTLIER_STD_THRESHOLD))
    return outlier_indices[0]


def _fill_forward(arr: np.array) -> np.array:
    mask = np.isnan(arr)
    indices_to_use = np.where(~mask, np.arange(mask.shape[0]), 0)
    np.maximum.accumulate(indices_to_use, axis=0, out=indices_to_use)
    return arr[indices_to_use]


def _rolling_average(arr: np.array, n: int) -> np.array:
    ret = np.cumsum(arr, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


@jit
def _rolling_std(arr: np.array, rolling_avg: np.array, n: int) -> np.array:
    variance = np.zeros(len(arr) - n + 1)
    assert len(variance) == len(rolling_avg)
    for i in range(len(variance)):
        variance[i] = np.sum(np.square(arr[i:i+n] - rolling_avg[i])) / n
    return np.sqrt(variance)


if __name__ == '__main__':
    _main()
