import argparse
import csv
import datetime
from typing import Optional

import h5py
import numpy as np


def _main():
    args = _parse_args()
    _run(args.input, args.measurement, args.threshold, args.output)


def _run(input_fname: str,
         measurement: str,
         threshold: float,
         output_fname: Optional[str]):
    input_file = h5py.File(input_fname, mode='r')

    print('Finding extreme values')
    measurements = input_file[measurement][:]
    extreme_indices = np.where(measurements > threshold)[0]
    print(
        f'Found {len(extreme_indices)} extreme values for measurement '
        f'{measurement}')

    if output_fname:
        print(f'Writing extremes to {output_fname}')
        timestamps = input_file['timestamp']
        station_ids = input_file['station_usaf']
        with open(output_fname, 'wt') as out_file:
            writer = csv.DictWriter(
                out_file,
                fieldnames=('station_usaf', 'timestamp', 'value'))
            writer.writerows([
                {
                    'station_usaf': station_ids[index],
                    'timestamp': datetime.datetime.utcfromtimestamp(
                        timestamps[index]),
                    'value': measurements[index]
                }
                for index in extreme_indices
            ])


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='path to input HDF5 file containing data to find extremes in')
    parser.add_argument(
        '-m', '--measurement',
        required=True,
        help='measurement to find extremes in')
    parser.add_argument(
        '-t', '--threshold',
        type=float,
        required=True,
        help='values greater than this arg are considered extreme')
    parser.add_argument(
        '-o', '--output',
        help='name of output CSV file that contains extremes')
    return parser.parse_args()


if __name__ == '__main__':
    _main()
