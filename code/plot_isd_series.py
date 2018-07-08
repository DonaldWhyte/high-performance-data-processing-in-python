import argparse
import datetime
import h5py
import matplotlib.pyplot as plt
import numpy as np


def _main():
    args = _parse_args()

    input_file = h5py.File(args.input, mode='r')

    indices_of_data = np.where(input_file['station_usaf'][:] == args.station)[0]
    if len(indices_of_data) == 0:
        print('No data to plot')
        return

    timestamps = [
        datetime.datetime.fromtimestamp(x)
        for x in input_file['timestamp'][indices_of_data]
    ]
    measurements = input_file[args.measurement][indices_of_data]

    plt.plot(timestamps, measurements)
    plt.title(f'station {args.station} {args.measurement}')
    plt.show()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='path to input HDF5 file containing time series to plot')
    parser.add_argument(
        '-s', '--station',
        required=True,
        help='USAF number of station to plot')
    parser.add_argument(
        '-m', '--measurement',
        required=True,
        help='measurement to plot')
    return parser.parse_args()


if __name__ == '__main__':
    _main()
