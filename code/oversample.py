"""
TODO: explain
"""

import argparse
import datetime
import csv
from typing import List, Tuple

import pandas as pd


_NON_MEASUREMENT_COLUMNS = {
    'STATION', 'STATION_NAME', 'ELEVATION', 'LATITUDE', 'LONGITUDE', 'DATE'
    #'STATION', 'DATE', 'SOURCE', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'NAME',
    #'REPORT_TYPE', 'CALL_SIGN', 'QUALITY_CONTROL'
}

def _main():
    args = _parse_args()
    step_size = {
        '1sec': 1,
        '5sec': 5,
        '10sec': 10,
        '30sec': 30,
        '1min': 60,
        '5min': 60 * 5,
        '10min': 60 * 10,
        '30min': 60 * 30
    }[args.granularity]

    df = pd.read_csv(args.input)
    df.sort_values(['STATION', 'DATE'], inplace=True)
    float_cols = list(df.select_dtypes(include=['float']).columns)
    rows = df.to_dict(orient='record')

    with open(args.output, 'wt') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        for a, b in zip(rows[:-1], rows[1:]):
            writer.writerow(a)
            if _primary_key(a) == _primary_key(b):
                a_dt = _to_dt(a['DATE'])
                b_dt = _to_dt(b['DATE'])

                # Based on the input granularity/step size, determine how many
                # samples to add between point a and b,
                n_steps = int((b_dt - a_dt).total_seconds() / step_size)
                interpolated_values = {
                    col: _interpolate(float(a[col]), float(b[col]), n_steps)
                    for col in a.keys() if col in float_cols
                }
                for step in range(1, n_steps):
                    row = {
                        col: val for col, val in a.items()
                        if col not in float_cols
                    }
                    row['DATE'] = (
                        (a_dt + datetime.timedelta(seconds=(step * step_size)))
                        .strftime(_DT_FORMAT))
                    row.update({
                        col: f'{interpolated_values[col][step]:.4f}'
                        for col in a.keys()
                        if col in float_cols
                    })
                    writer.writerow(row)

        # Need to write the final row of the input CSV after the interpolation
        # loop.
        writer.writerow(b)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='path to input file to oversample')
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='path of oversampled file to generate')
    parser.add_argument(
        '-g', '--granularity',
        required=True,
        choices=('1min', '10min'),
        help='granularity of oversampling. This determines how many extra '
             'samples will be generated between two time points.')
    return parser.parse_args()



def _primary_key(row: dict) -> Tuple[str, str]:
    return row['STATION']


def _to_dt(val: str) -> datetime.datetime:
    return datetime.datetime.strptime(val, _DT_FORMAT)


_DT_FORMAT = '%Y-%m-%dT%H:%M%S'


def _interpolate(start: float, end: float, n_steps: int) -> List[float]:
    step_size = (end - start) / n_steps
    return [start + step_size * step for step in range(n_steps)]


if __name__ == '__main__':
    _main()
