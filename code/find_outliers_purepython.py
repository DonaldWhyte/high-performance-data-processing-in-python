import argparse
import csv
import datetime
import math
import time


_DIFFERENCE_RANGE = 1
_ROLLING_WINDOW = 14 * 6  # 7 days
_OUTLIER_STD_THRESHOLD = 9


def _main():
    args = _parse_args()

    with open(args.input, 'rt') as input_file:
        rows = [
            (row['station_usaf'], row['timestamp'], row[args.measurement])
            for row in csv.DictReader(input_file)
        ]

    start_time = time.time()

    print('Determining range of each station time series')
    series_ranges = []
    current_start = 0
    current_station_id = row['station_usaf'][0]
    for i in range(1, len(rows)):
        station_id = rows[i]['station_usaf']
        if current_station_id != station_id:
            series_ranges.append((current_start, i))
            current_start = i
        current_station_id = station_id

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
    station_outliers = {
        station_ids[start]: _compute_outliers(rows[start:end],
                                              _ROL3LING_WINDOW)
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


def _compute_outliers(data: List[dict], n: int) -> np.array:
    data = _fill_forward(data)

    #differenced = [
    #    curr - prev
    #    for prev, curr in zip(data[:-_DIFFERENCE_RANGE],
    #                          data[_DIFFERENCE_RANGE:])
    #]

    avg = _rolling_average(data, n)
    std = _rolling_standard_deviation(data, avg, n)
    series_with_std = data[n - 1:]

    return [
        i for i in range(len(differences_with_std))
        if math.fabs(series_with_std[i] - avg[i] >
                     (std * _OUTLIER_STD_THRESHOLD))
    ]


def _fill_forward(data: List[dict]):
    prev_val = data[0]
    for i in range(1, len(data)):
        if math.isnan(data[i]):
            data[i] = prev_val
        prev_val = data[i]


def _rolling_average(data: List[dict], n: int) -> List[float]:
    averages = [0 for i in range(len(data)) - n]
    numerator = sum(data[:n])
    denominator = n
    for i in range(len(averages)):
        numerator = numerator + data[i] - data[i - n]
        averages[i] = numerator / denominator
    return averages


def _rolling_standard_deviation(data: List[data],
                                averages: List[float],
                                n: int) -> List[float]:
    differences_to_avg = data[i] - averages[i]
    return [
        math.sqrt(sum(TODO - averages[i]) ** 2))
    ]


    variance = np.zeros(len(arr) - n + 1)
    assert len(variance) == len(rolling_avg)
    for i in range(len(variance)):
        variance[i] = np.sum(np.square(arr[i:i+n] - rolling_avg[i])) / n
    return np.sqrt(variance)



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
        required=True,
        help='name of output CSV file that contains outliers')
    return parser.parse_args()


if __name__ == '__main__':
    _main()
