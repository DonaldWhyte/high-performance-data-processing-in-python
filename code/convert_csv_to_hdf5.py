import argparse
import csv
import datetime
#import h5py
import itertools
import math
import numpy as np
import pandas as pd
from typing import Optional


_BATCH_SIZE = 100000


def _float_converter(x: float) -> float:
    return np.nan if x in _NAN_VALUES else float(x)


_NAN_VALUES = {'-9999.0', '-9999'}


_COLUMN_CONVERTERS = {
    'timestamp': lambda x:
        datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').timestamp(),
    'station_usaf': lambda x: int(x),
    'station_wban': lambda x: int(x),
    'air_temperature': _float_converter,
    'dew_point_temperature': _float_converter,
    'sea_level_pressure': _float_converter,
    'wind_direction': _float_converter,
    'wind_speed_rate': _float_converter,
    'sky_condition': _float_converter,
    'liquid_precipitation_1h': _float_converter,
    'liquid_precipitation_6h': _float_converter
}


def _main():
    args = _parse_args()
    with open(args.input, 'rt') as in_file:
        reader = csv.DictReader(in_file)
        #out_hdf5 = h5py.File(args.output)
        out_hdf5 = pd.HDFStore(args.output)
        for i, row_batch in enumerate(_batch(reader, _BATCH_SIZE)):
            print(f'Processed {i * _BATCH_SIZE} rows')
            for col, converter in _COLUMN_CONVERTERS.items():
                records = [
                    {
                        col: converter(row[col])
                        for col, converter in _COLUMN_CONVERTERS.items()
                    }
                    for row in row_batch
                ]
                out_hdf5.append(
                    'isdlite',
                    pd.DataFrame(records),
                    data_columns=sorted(_COLUMN_CONVERTERS.keys()),
                    format='table')
                """_create_or_append_to_dataset(
                    out_hdf5,
                    name=col,
                    data=np.array([
                        converter(row[col]) for row in row_batch
                    ]))"""
            #out_hdf5.flush()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='path to input archive to process')
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='path of combined CSV file to generate')
    return parser.parse_args()


def _batch(iterable, n):
    iterator = iter(iterable)
    yield from iter(lambda: list(itertools.islice(iterator, n)), [])


"""def _create_or_append_to_dataset(hdf5_file: h5py.File,
                                 name: str,
                                 data: np.ndarray):
    if name in hdf5_file:
        old_len = len(hdf5_file[name])
        hdf5_file[name].resize(old_len + len(data), axis=0)
        hdf5_file[name][old_len:] = data
    else:
        hdf5_file.create_dataset(
            name,
            data=data,
            maxshape=(None,),
            compression='gzip')"""


if __name__ == '__main__':
    _main()
