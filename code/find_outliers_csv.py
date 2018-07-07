import argparse
import datetime
import matplotlib.pyplot as plt
import pandas as pd


def _main():
    args = _parse_args()

    print()
    store = pd.read_hdf(args.input, mode='r')
    df = pd.read_hdf(
        'isdlite_table.h5',
        'isdlite',
        columns=['timestamp', args.measurement],
        where=[f'station_usaf=={args.station}'])
    df['timestamp'] = df['timestamp'].apply(datetime.datetime.fromtimestamp)
    df.sort_values('timestamp', inplace=True)

    plt.plot(df['timestamp'], df[args.measurement])
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
