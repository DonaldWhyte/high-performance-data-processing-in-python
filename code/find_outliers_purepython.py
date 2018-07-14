import argparse
import csv
import datetime
import h5py
import math
import time
from typing import List, Optional, Tuple


_DIFFERENCE_RANGE = 1
_ROLLING_WINDOW = 14 * 6  # 7 days
_OUTLIER_STD_THRESHOLD = 9


def _main():
    args = _parse_args()
    _run(args.input, args.measurement, args.output)


def _run(input_fname: str, measurement: str, output_fname: Optional[str]):
    # Load input data before starting timer. We're only interested in measuring
    # computation time, not disk IO or memory speed.
    input_file = h5py.File(input_fname, mode='r')
    station_ids = list(input_file['station_usaf'][:])
    measurements = list(input_file[measurement][:])

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
    station_outliers = {
        station_ids[start]: compute_outliers(measurements[start:end],
                                             _ROLLING_WINDOW)
        for start, end in ranges_with_enough_data
    }

    elapsed_time = time.time() - start_time
    print(f'Computed outliers in {elapsed_time:.2f} seconds')

    if output_fname:
        print(f'Writing outliers to {output_fname}')
        timestamps = list(input_file['timestamp'][:])
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


def series_ranges(station_ids: List[int]) -> List[Tuple[int, int]]:
    ranges = []
    current_start = 0
    current_station_id = station_ids[0]
    for i in range(1, len(station_ids)):
        if current_station_id != station_ids[i]:
            ranges.append((current_start, i))
            current_start = i
        current_station_id = station_ids[i]
    # At the end of the loop create the final series range, which represents
    # the last station series in the data.
    ranges.append((current_start, i))

    return ranges


def compute_outliers(data: List[dict], n: int) -> List[int]:
    fill_forward(data)
    series_with_averages = data[n:]
    avg = rolling_average(data, n)
    std = rolling_standard_deviation(data, avg, n)
    return find_outliers(series_with_averages, avg, std)


def fill_forward(data: List[dict]):
    prev_val = data[0]
    for i in range(1, len(data)):
        if math.isnan(data[i]):
            data[i] = prev_val
        prev_val = data[i]


def rolling_average(data: List[dict], n: int) -> List[float]:
    averages = [0 for i in range(len(data) - n)]
    numerator = sum(data[:n])
    denominator = n
    for i in range(len(averages)):
        numerator = numerator + data[i] - data[i - n]
        averages[i] = numerator / denominator
    return averages


def rolling_standard_deviation(data: List[float],
                                averages: List[float],
                                n: int) -> List[float]:
    return [
        math.sqrt(sum(_squared_diffs(data[i:i+n], averages[i])) / n)
        for i in range(len(data) - n)
    ]


def _squared_diffs(data: List[float], avg: float) -> List[float]:
    return [math.pow(value - avg, 2) for value in data]


def find_outliers(series_with_avgs: List[float],
                  rolling_avg: List[float],
                  rolling_std: List[float]) -> List[int]:
    return [
        i for i in range(len(series_with_avgs))
        if math.fabs(series_with_avgs[i] - rolling_avg[i] >
                     (rolling_std[i] * _OUTLIER_STD_THRESHOLD))
    ]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='path to input CSV file containing time series to find outliers '
             'in')
    parser.add_argument(
        '-m', '--measurement',
        required=True,
        help='measurement to plot')
    parser.add_argument(
        '-o', '--output',
        help='name of output CSV file that contains outliers')
    return parser.parse_args()


if __name__ == '__main__':
    _main()
