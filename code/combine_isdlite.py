import argparse
import csv
import datetime
from io import TextIOWrapper
import tarfile
import tempfile


_OUTPUT_COLUMNS = (
    'timestamp',
    'air_temperature',
    'dew_point_temperature',
    'sea_level_pressure',
    'wind_direction',
    'wind_speed_rate',
    'sky_condition',
    'liquid_precipitation_1h',
    'liquid_precipitation_6h'
)


def _main():
    args = _parse_args()

    with open(args.output, 'wt') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=_OUTPUT_COLUMNS)
        writer.writeheader()

        archive = tarfile.open(args.input, mode='r:gz')
        for i, fname in enumerate(archive.getnames()):
            if i % 1000 == 0:
                print(f'Processed {i} files')

            fname_components = fname.split('-')
            if len(filename_components) == 3:
                writer.writerows([
                    _process_line(
                        line,
                        station_usaf=fname_components[0],
                        station_wban=fname_components[1])
                    for line in TextIOWrapper(archive.extractfile(fname)).readlines()
                ])


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


def _process_line(line: str,
                  station_usaf: str,
                  station_wban: str) -> dict:
    fields = line.split()
    date_components = [x for x in fields[:4]]
    timestamp = datetime.datetime.strptime(
        ' '.join(date_components), '%Y %m %d %H')
    return {
        'station_usaf': station_usaf,
        'station_wban': station_wban,
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'air_temperature': float(fields[4]),
        'dew_point_temperature': float(fields[5]),
        'sea_level_pressure': float(fields[6]),
        'wind_direction': float(fields[7]),
        'wind_speed_rate': float(fields[8]),
        'sky_condition': float(fields[9]),
        'liquid_precipitation_1h': float(fields[10]),
        'liquid_precipitation_6h': float(fields[11])
    }


if __name__ == '__main__':
    _main()
