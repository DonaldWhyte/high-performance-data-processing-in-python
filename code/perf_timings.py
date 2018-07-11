from statistics import mean, stdev
from timeit import repeat


_NUM_TESTS = 5


def _main():
    list_add_indexing = repeat(
        '''\
c = [a[i] + b[i] for i in range(len(a))]
        ''',
        setup='a = list(range(10000000)); b = list(range(10000000))',
        number=1,
        repeat=_NUM_TESTS)

    list_add_zip = repeat(
        '''\
c = [x + y for x, y in zip(a, b)]
        ''',
        setup='''\
a = list(range(10000000))
b = list(range(10000000))
        ''',
        number=1,
        repeat=_NUM_TESTS)

    numpy_add_loop = repeat(
        '''\
c = np.zeros(len(a))
for i in range(len(a)):
    c[i] = a[i] + b[i]
        ''',
        setup='''\
import numpy as np
a = np.arange(10000000)
b = np.arange(10000000)
        ''',
        number=1,
        repeat=_NUM_TESTS)

    numpy_add_vectorised = repeat(
        '''\
a + b
        ''',
        setup='''\
import numpy as np
a = np.arange(10000000)
b = np.arange(10000000)
        ''',
        number=1,
        repeat=_NUM_TESTS)

    _print_times('Adding two lists (indexing)', list_add_indexing)
    _print_times('Adding two lists (zip)', list_add_zip)
    _print_times('Adding two numpy arrays (loop)', numpy_add_loop)
    _print_times('Adding two numpy arrays (numpy)', numpy_add_vectorised)


def _print_times(test_name, times):
    print(
        f'{test_name}: min={min(times):.4f}s, max={max(times):.4f}s, '
        f'avg={mean(times):.4f}s, stddev={stdev(times):.4f}s')


if __name__ == '__main__':
    _main()
