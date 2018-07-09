import argparse
import datetime
import h5py
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np


def _main():
    args = _parse_args()

    input_file = h5py.File(args.input, mode='r')

    station_indices = np.where(input_file['station_usaf'][:] == args.station)[0]

    start_dt = args.start_date.timestamp()
    ts_indices = np.where(input_file['timestamp'][:] > start_dt)[0]

    data_indices = np.intersect1d(station_indices, ts_indices)
    if len(data_indices) == 0:
        print('No data to plot')
        return

    timestamps = [
        datetime.datetime.fromtimestamp(x)
        for x in input_file['timestamp'][:][data_indices]
    ]
    measurements = input_file[args.measurement][:][data_indices]

    _, ax = plt.subplots()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
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
        type=int,
        required=True,
        help='USAF number of station to plot')
    parser.add_argument(
        '-m', '--measurement',
        required=True,
        help='measurement to plot')
    parser.add_argument(
        '--start_date',
        type=lambda x: datetime.datetime.strptime(x, '%Y%m%d'),
        default=datetime.datetime(1970, 1, 1, 0, 0),
        help='only plot data at or after this date')
    return parser.parse_args()



if __name__ == '__main__':
    _main()
