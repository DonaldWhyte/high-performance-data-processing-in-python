import csv
import os
import posixpath
import prettytable
import typing

import numpy as np
import numpy_indexed as npi


_STOCK_DIR = 'Stocks'
_FILE_SUFFIX = '.us.txt'


class PriceMatrix:

	def __init__(self, dates: np.ndarray, symbols: typing.List[str]):
		self.dates = dates
		self.symbols = symbols
		self.prices = np.ndarray(shape=(len(self.dates), len(self.symbols)))

	@property
	def shape(self):
		return self.prices.shape

	def __str__(self):
		table = prettytable.PrettyTable()
		table.field_names = ['date'] + [s.upper() for s in self.symbols]
		for date_index, prices_on_date in enumerate(self.prices):
			table.add_row([self.dates[date_index]] + list(prices_on_date))
		return str(table)

	def __repr__(self):
		return str(self)


def _main():
	# Determine all trading dates that belong in the simulation.
	start = np.datetime64('1990-01-01')
	end = np.datetime64('2017-11-11')
	dates = _filter_to_business_days(np.arange(start, end))

	# Determine all symbols which have market data in the sim date range.
	stock_files = sorted(os.listdir(_STOCK_DIR))[:10]
	symbols = [
		fname.replace(_FILE_SUFFIX, '')
		for fname in stock_files
		if (fname.endswith(_FILE_SUFFIX) and
			_has_data_in_range(posixpath.join(_STOCK_DIR, fname), start, end))
	]

	#  Construct pricing matrix.
	pmat = PriceMatrix(dates, symbols)
	print(f'Price matrix shape: {pmat.shape}')

	for symbol_index, symbol in enumerate(symbols):
		stock_prices = _load_stock_prices(dates, symbol)
		pmat.prices[:, symbol_index] = _fill_forward(stock_prices)

	print(pmat)


def _filter_to_business_days(dates):
	# only weekdays
	dates = dates[np.where(np.is_busday(dates))]
	# only US trading days
	dates = dates[np.where(np.isin(dates,	
								   _US_HOLIDAYS,
								   invert=True,
								   assume_unique=True))] 
	return dates


def _fill_forward(arr):
    mask = np.isnan(arr)
    indices_to_use = np.where(~mask, np.arange(mask.shape[0]), np.array([0]))
    np.maximum.accumulate(indices_to_use, axis=0, out=indices_to_use)
    return arr[indices_to_use]


def _has_data_in_range(fname, start, end):
	print(f'Checking if file {fname} has data in range {start} - {end}')
	contents = open(fname).read().strip()
	if len(contents) > 0:
		timestamps = _load_dates_from_price_file(fname)
		min_d = timestamps.min() 
		max_d = timestamps.max()
		return start <= max_d and min_d <= end
	else:
		return False


def _load_stock_prices(dates, symbol):
	print(f'Loading pricing data for stock {symbol.upper()}')

	symbol_dates = _filter_to_business_days(
		_load_dates_from_price_file(f'{_STOCK_DIR}/{symbol}.us.txt'))
	mat_idx_to_file_idx = npi.indices(symbol_dates, dates, missing=-1)

	missing_indices = np.where(mat_idx_to_file_idx == -1)
	if len(missing_indices) > 0:
		missing_dates = [
			str(d)[:10] for d in sorted(set(dates[missing_indices]))
		]
		print(
			f'Missing pricing data for stock {symbol.upper()} for '
			f'the following dates: {missing_dates})')

	file_prices = np.zeros(shape=(len(symbol_dates) + 1,))
	file_prices[:-1] = np.loadtxt(
	    f'Stocks/{symbol}.us.txt',
	    skiprows=1,       # skip CSV header  
	    delimiter=',',
	    usecols=4,
	    dtype=np.float64)
	file_prices[-1] = np.nan

	return file_prices[mat_idx_to_file_idx]


def _load_dates_from_price_file(fname):
	return np.loadtxt(
	    fname,
	    skiprows=1,       # skip CSV header  
	    delimiter=',',
	    usecols=0,
	    dtype=np.datetime64)


_US_HOLIDAYS = np.array(
	(
		'1990-01-01',
		'1990-02-19',
		'1990-04-13',
		'1990-05-28',
		'1990-07-04',
		'1990-09-03',
		'1990-11-22',
		'1990-12-25',
		'1991-01-01',
		'1991-02-18',
		'1991-03-29',
		'1991-05-27',
		'1991-07-04',
		'1991-09-02',
		'1991-11-28',
		'1991-12-25',
		'1992-01-01',
		'1992-02-17',
		'1992-04-17',
		'1992-05-25',
		'1992-07-03',
		'1992-09-07',
		'1992-11-26',
		'1992-12-25',
		'1993-01-01',
		'1993-02-15',
		'1993-04-09',
		'1993-05-31',
		'1993-07-05',
		'1993-09-06',
		'1993-11-25',
		'1993-12-24',
		'1994-02-21',
		'1994-04-01',
		'1994-04-27',
		'1994-05-30',
		'1994-07-04',
		'1994-09-05',
		'1994-11-24',
		'1994-12-26',
		'1995-01-02',
		'1995-02-20',
		'1995-04-14',
		'1995-05-29',
		'1995-07-04',
		'1995-09-04',
		'1995-11-23',
		'1995-12-25',
		'1996-01-01',
		'1996-02-19',
		'1996-04-05',
		'1996-05-27',
		'1996-07-04',
		'1996-09-02',
		'1996-11-28',
		'1996-12-25',
		'1997-01-01',
		'1997-02-17',
		'1997-03-28',
		'1997-05-26',
		'1997-07-04',
		'1997-09-01',
		'1997-11-27',
		'1997-12-25',
		'1998-01-01',
		'1998-01-19',
		'1998-02-16',
		'1998-04-10',
		'1998-05-25',
		'1998-07-03',
		'1998-09-07',
		'1998-11-26',
		'1998-12-25',
		'1999-01-01',
		'1999-01-18',
		'1999-02-15',
		'1999-04-02',
		'1999-05-31',
		'1999-07-05',
		'1999-09-06',
		'1999-11-25',
		'1999-12-24',
		'2000-01-17',
		'2000-02-21',
		'2000-04-21',
		'2000-05-29',
		'2000-07-04',
		'2000-09-04',
		'2000-11-23',
		'2000-12-25',
		'2001-01-01',
		'2001-01-15',
		'2001-02-19',
		'2001-04-13',
		'2001-05-28',
		'2001-07-04',
		'2001-09-03',
		'2001-09-11',
		'2001-09-12',
		'2001-09-13',
		'2001-09-14',
		'2001-11-22',
		'2001-12-25',
		'2002-01-01',
		'2002-01-21',
		'2002-02-18',
		'2002-03-29',
		'2002-05-27',
		'2002-07-04',
		'2002-09-02',
		'2002-11-28',
		'2002-12-25',
		'2003-01-01',
		'2003-01-20',
		'2003-02-17',
		'2003-04-18',
		'2003-05-26',
		'2003-07-04',
		'2003-09-01',
		'2003-11-27',
		'2003-12-25',
		'2004-01-01',
		'2004-01-19',
		'2004-02-16',
		'2004-04-09',
		'2004-05-31',
		'2004-06-11',
		'2004-07-05',
		'2004-09-06',
		'2004-11-25',
		'2004-12-24',
		'2005-01-17',
		'2005-02-21',
		'2005-03-25',
		'2005-05-30',
		'2005-07-04',
		'2005-09-05',
		'2005-11-24',
		'2005-12-26',
		'2006-01-02',
		'2006-01-16',
		'2006-02-20',
		'2006-04-14',
		'2006-05-29',
		'2006-07-04',
		'2006-09-04',
		'2006-11-23',
		'2006-12-25',
		'2007-01-01',
		'2007-01-02',
		'2007-01-15',
		'2007-02-19',
		'2007-04-06',
		'2007-05-28',
		'2007-07-04',
		'2007-09-03',
		'2007-11-22',
		'2007-12-25',
		'2008-01-01',
		'2008-01-21',
		'2008-02-18',
		'2008-03-21',
		'2008-05-26',
		'2008-07-04',
		'2008-09-01',
		'2008-11-27',
		'2008-12-25',
		'2009-01-01',
		'2009-01-19',
		'2009-02-16',
		'2009-04-10',
		'2009-05-25',
		'2009-07-03',
		'2009-09-07',
		'2009-11-26',
		'2009-12-25',
		'2010-01-01',
		'2010-01-18',
		'2010-02-15',
		'2010-04-02',
		'2010-05-31',
		'2010-07-05',
		'2010-09-06',
		'2010-11-25',
		'2010-12-24',
		'2011-01-17',
		'2011-02-21',
		'2011-04-22',
		'2011-05-30',
		'2011-07-04',
		'2011-09-05',
		'2011-11-24',
		'2011-12-26',
		'2012-01-02',
		'2012-01-16',
		'2012-02-20',
		'2012-04-06',
		'2012-05-28',
		'2012-07-04',
		'2012-09-03',
		'2012-10-29',
		'2012-10-30',
		'2012-11-22',
		'2012-12-25',
		'2013-01-01',
		'2013-01-21',
		'2013-02-18',
		'2013-03-29',
		'2013-05-27',
		'2013-07-04',
		'2013-09-02',
		'2013-11-28',
		'2013-12-25',
		'2014-01-01',
		'2014-01-20',
		'2014-02-17',
		'2014-04-18',
		'2014-05-26',
		'2014-07-04',
		'2014-09-01',
		'2014-11-27',
		'2014-12-25',
		'2015-01-01',
		'2015-01-19',
		'2015-02-16',
		'2015-04-03',
		'2015-05-25',
		'2015-07-03',
		'2015-09-07',
		'2015-11-26',
		'2015-12-25',
		'2016-01-01',
		'2016-01-18',
		'2016-02-15',
		'2016-03-25',
		'2016-05-30',
		'2016-07-04',
		'2016-09-05',
		'2016-11-24',
		'2016-12-26',
		'2017-01-02',
		'2017-01-16',
		'2017-02-20',
		'2017-04-14',
		'2017-05-29',
		'2017-07-04',
		'2017-09-04',
		'2017-11-23',
		'2017-12-25',
		'2018-01-01',
		'2018-01-15',
		'2018-02-19',
		'2018-03-30',
		'2018-05-28',
		'2018-07-04',
		'2018-09-03',
		'2018-11-22',
		'2018-12-25',
		'2019-01-01',
		'2019-01-21',
		'2019-02-18',
		'2019-04-19',
		'2019-05-27',
		'2019-07-04',
		'2019-09-02'
	),
	dtype=np.datetime64)


if __name__ == '__main__':
	_main()