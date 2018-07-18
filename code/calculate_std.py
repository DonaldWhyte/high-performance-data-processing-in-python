import math


def _main():
    a = list(range(100000000))
    _std(a)

def _std(a):
    mean = _mean(a)
    squared_differences = _square(_differences(a, mean))
    sum_of_sq_diffs = _sum(squared_differences)
    return math.sqrt(sum_of_sq_diffs / len(a) - 1)

def _mean(a):
    return _sum(a) / len(a)

def _differences(a, mean):
    return [x - mean for x in a]

def _square(a):
    return [x * x for x in a]

def _sum(a):
    s = 0
    for x in a:
        s += x
    return s

def _divide(a, d):
    return [x / d for x in a]


if __name__ == '__main__':
    _main()
