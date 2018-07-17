import numpy as np


def _main():
    # Inputs
    n = 3
    x = np.arange(20, dtype=np.float64)

    # Slow average/std
    avg = np.zeros(len(x) - n + 1)
    std = np.zeros(len(x) - n + 1)
    for i in range(len(avg)):
        avg[i] = np.mean(x[i:i+n])
        std[i] = np.std(x[i:i+n])

    print('AVG')
    print('\n'.join(str(x) for x in avg))
    print('STD:')
    print('\n'.join(str(x) for x in std))

    # Fast std
    squares = np.square(x)
    sum_of_squares = np.convolve(squares, np.ones(n, dtype=int), 'valid')
    var_fast = (sum_of_squares / n) - np.square(avg)
    std_fast = np.sqrt(var_fast)

    print('STD FAST:')
    print('\n'.join(str(x) for x in std_fast))


if __name__ == '__main__':
    _main()
