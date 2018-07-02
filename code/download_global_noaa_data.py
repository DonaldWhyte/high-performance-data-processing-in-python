import argparse
import csv
import datetime
import os
import random
import tarfile
import tempfile
import time
import urllib.request


_ROOT_URL = 'https://www.ncei.noaa.gov/data/global-hourly/archive/'


def _main():
    args = _parse_args()
    years = [
        args.start_year + i for i in range(args.end_year - args.start_year + 1)
    ]
    print(f'Downloading data for years: {years}')

    with open(args.output, 'w') as out_file:
        writer = csv.DictWriter(out_file, extrasaction='raise', fieldnames=[
            "STATION",
            "DATE",
            "SOURCE",
            "LATITUDE",
            "LONGITUDE",
            "ELEVATION",
            "NAME",
            "REPORT_TYPE",
            "CALL_SIGN",
            "QUALITY_CONTROL",
            "WND",
            "CIG",
            "VIS",
            "TMP",
            "DEW",
            "SLP",
            "GF1",
            "MW1",
            "EQD"
        ])
        writer.writeheader()

        for year in years:
            url = f'{_ROOT_URL}{year}.tar.gz'
            print(f'Downloading {url}')
            with urllib.request.urlopen(url) as archive_file:
                with tempfile.NamedTemporaryFile() as tmpfile:
                    tmpfile.write(archive_file.read())
                    tmpfile.flush()
                    print(f'Extracting {url}')
                    with tempfile.TemporaryDirectory() as tmpdir:
                        tarfile.open(tmpfile.name).extractall(path=tmpdir)
                        for fname in os.listdir(tmpdir):
                            print(f'Processing {fname}')
                            fpath = os.path.join(tmpdir, fname)
                            with open(fpath, 'r') as in_file:
                                reader = csv.DictReader(
                                    in_file,
                                    quotechar='"',
                                    delimiter=',',
                                    skipinitialspace=True)
                                #for row in reader:
                                #    print(f'\t{row}')
                                writer.writerows(list(reader))

            # Sleep for some interval to prevent overloading the source site.
            time.sleep(random.uniform(1, 2))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s', '--start_year',
        type=int,
        required=True,
        help='start of range of years to download data for')
    parser.add_argument(
        '-e', '--end_year',
        type=int,
        required=True,
        help='end of range of years to download data for')
    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='path to output CSV file that will contain all data retrieved '
             'for the specified range of years')
    return parser.parse_args()


if __name__ == '__main__':
    _main()
