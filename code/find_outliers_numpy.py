import argparse
import datetime
import h5py
from multiprocessing import Pool
from numba import jit
import numpy as np
from typing import Optional


_DIFFERENCE_RANGE = 4
_ROLLING_WINDOW = 7 * 6  # 7 days
_OUTLIER_STD_THRESHOLD = 6


def _main():
    args = _parse_args()
    _run(args.input, args.measurement, args.display)


def _run(input_fname: str, measurement: str, display_mode: Optional[str]):
    input_file = h5py.File(input_fname, mode='r')

    print('Determining range of each station time series')
    station_ids = input_file['station_usaf'][:10000000]
    is_end_of_series = station_ids[:-1] != station_ids[1:]
    series_ends = np.where(is_end_of_series == True)[0]
    series_starts = np.concatenate([np.array([0]), series_ends + 1])
    series_ranges = list(zip(series_starts, series_ends))
    print('Found time series for', len(series_ranges), 'ranges')

    print('Removing time series that don\'t have enough daa')
    ranges_with_enough_data = [(start, end) for start, end in series_ranges]
    print(
        'Kept', len(ranges_with_enough_data), '/', len(series_ranges),
        'station time series')

    print('Computing outliers')
    measurements = input_file[measurement]
    station_outliers = {
        station_ids[start]: _compute_outliers(measurements[start:end],
                                              _ROLLING_WINDOW)
        for start, end in ranges_with_enough_data
        if end - start >= (_DIFFERENCE_RANGE + _ROLLING_WINDOW + 1)
    }

    if display_mode:
        display_detailed = display_mode == 'detail'

        timestamps = input_file['timestamp']
        for station, outlier_indices in station_outliers.items():
            print(station, 'has', len(outlier_indices), 'outliers')
            if display_detailed:
                for index in outlier_indices:
                    print('\t', index, timestamps[index], measurements[index])


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='path to input HDF5 file containing time series to plot')
    parser.add_argument(
        '-m', '--measurement',
        required=True,
        help='measurement to plot')
    parser.add_argument(
        '-d', '--display',
        choices=('summary', 'detail'),
        help='display detailed information about all found outliers')
    return parser.parse_args()


def _compute_outliers(data: np.array, n: int) -> np.array:
    data = _fill_forward(data)

    shifted = data[:-_DIFFERENCE_RANGE]
    differenced = data[_DIFFERENCE_RANGE:] - shifted

    avg = _rolling_average(differenced, n)
    std = _rolling_standard_deviation(differenced, avg, n)
    differences_with_std = differenced[n - 1:]

    print(len(differences_with_std), len(avg), len(std))
    with open('data', 'wt') as f:
        f.write('\n.'.join(
            f'{differences_with_std[i]}, {avg[i]}, {std[i]}'
            for i in range(len(differences_with_std))
        ))
    raise ValueError

    outlier_indices = np.where(
        np.absolute(data_with_averages - avg) > (std * _OUTLIER_STD_THRESHOLD))
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
def _rolling_standard_deviation(arr: np.array,
                                rolling_avg: np.array,
                                n: int) -> np.array:
    variance = np.zeros(len(arr) - n + 1)
    assert len(variance) == len(rolling_avg)
    for i in range(len(variance)):
        print(i, len(arr[i:i+n]), rolling_avg[i], arr[i])
        variance[i] = np.sum(arr[i:i+n] - rolling_avg[i]) / n
    return np.sqrt(variance)


if __name__ == '__main__':
    _main()
