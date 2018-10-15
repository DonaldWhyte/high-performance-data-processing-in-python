<!-- .slide: data-background="images/intro_background.png" class="background" -->
### **Высокоэффективная обработка данных в Phyton**

#### High Performance Data Processing In Python

<p>
  <a href="http://twitter.com/donald_whyte">@donald_whyte</a>
</p>

<div id="logo-notice">
  <img src="images/moscow_python_confpp.png" alt="moscow_python_confpp" />
</div>

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
### About Me

<div class="left-col">
  ![small_portrait](images/donald.jpg)
</div>
<div class="right-col" style="text-center: left">
  <ul>
    <li>Software Engineer</li>
    <li>@ Engineers Gate</li>
    <li>Scalable data infrastructure</li>
    <li>Real-time trading systems</li>
    <li>Python/C++/Rust developer</li>
  </ul>
</div>
<div class="clear-col"></div>

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
**Python is a hugely popular tool for data analysis.**

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->

> **Data analysis is now as popular as web development with Python.**

<div class="reference">
  *JetBrains Python Developer Survey 2017* **[1]**
</div>

_note_
https://www.jetbrains.com/research/python-developers-survey-2017/

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
## Why?

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
## Suitable for **Research**

High-level and easy to use.

Doesn't require advanced programming knowledge.

Enables researchers to iterate on ideas quickly.

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
## Suitable for **Production**

General-purpose language useful outside of data analysis.

Huge ecosystem of packages for deploying prod systems.

Deployment, logging, profiling and monitoring.

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
## Python's Strength
Python suitable for **both use cases**.

Enables researchers to run experiments quickly.

Good tools for building prod-ready systems.

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background large-slide" -->
We want to use the same code

for prod **and** research!

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background large-slide" -->
But...

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background large-slide" -->
**Pure Python is slow.**

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
### Python vs. C Performance
<div id="python-vs-c-speedups"></div>

<div class="source">
  <p>
    Source: [The Computer Language Benchmarks Game](https://benchmarksgame-team.pages.debian.net/benchmarksgame/faster/python3-gcc.html)
  </p>
</div>

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background large-slide" -->
# Bad for Research

Very slow experimentation cycles.

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background large-slide" -->
# Bad for Production

Cannot run time-sensitive data processing or computational tasks.

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background large-slide" -->
# Solution
Python's data processing ecosystem.

[NEXT]
<!-- .slide: data-background="images/ecosystem.png" -->

[NEXT]
<!-- .slide: data-background="images/ecosystem_marked.png" -->

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
## NumPy

<div class="left-col">
  <ul>
    <li>Heart of scientific computing in Python</li>
    <li>Stores and operates on data in C structures</li>
    <li>Avoids slowness of Python</li>
  </ul>
</div>
<div class="right-col">
  <div style="height: 20px"></div>
  <img src="images/numpy_coloured.svg" alt="numpy_coloured" />
</div>
<div class="clear-col"></div>

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
Foundation of most scientific computing packages.

![scipy](images/scipy.svg)
![pandas](images/pandas.svg)
![sklearn](images/sklearn.svg)
![matplotlib](images/matplotlib.svg)

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
## Our Focus

Showing how to use NumPy to process numerical data.

Exploring how NumPy uses vectorisation to dramatically boost performance.

While still keeping Python productive.

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
## Outline

1. Build algo trading strategy using stock price data
2. Process stock price data in **pure Python**
3. Speed up processing using **NumPy** and vectorisation
4. Speed up processing even more using **Numba**

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background large-slide" -->
## Final Optimised Solution

TIME times faster than pure Python.


[NEXT SECTION]
## 1. Let's Make Some Cash
![upward_trend](images/upward_trend.svg)

[NEXT]
<div class="left-col" style="text-center: left">
  <br />
  <p>Use our programmer skills to make money...</p>
  <p>...by building an <strong>automated stock trading strategy!</strong></p>
</div>
<div class="right-col">
  ![quant](images/quant.jpg)
</div>
<div class="clear-col"></div>

[NEXT]
# The Data

[NEXT]
<!-- .slide: class="large-slide" -->
**Prices of 7000+ US stocks.**

**From 1962 to 2017.**

[NEXT]
<!-- .slide: class="medium-slide" -->
Collection of **CSV** files.

<img src="images/daily_price_list.svg" alt="daily_price_files" />

[NEXT]
`aapl.us.txt`

![price_csv](images/price_csv.png)

[NEXT]
![aapl_price_graph](images/aapl_price_graph.svg)

[NEXT]
<!-- .slide: class="large-slide" -->
## Total Dataset Size

Over 6,000,000 rows.

1 gigabyte.


[NEXT]
## Goal
Build an program that generates **lists of trades** to make.

One trade list **every day!**

[NEXT]
## How?
We leverage **two fundamental behaviours** about stock prices.

[NEXT]
## 1. Prices Revert to the Mean

[NEXT]
![mean_reversion](images/mean_reversion.png)

[NEXT]
![reversion_example_aapl](images/reversion_example_aapl_price.svg)

[NEXT]
### Stock's Absolute Daily Return

<div>
Stock's price is:

![equation](images/equation_stockprice.svg)
</div> <!-- .element: class="fragment" data-fragment-index="0" -->

<div>
Stock's absolute daily return (in USD) on day _t_ is:

![equation](images/equation_absolute_returns.svg)
</div> <!-- .element: class="fragment" data-fragment-index="1" -->


_note_
equation is today's price - yesterday's price / yesterday's price

[NEXT]
![reversion_example_aapl](images/reversion_example_aapl_abs_return.svg)

[NEXT]
TODO: return graph with outlier boundary lines

[NEXT]
TODO: return graph with first outlier highlighted (buy)

[NEXT]
TODO: return graph with sell point highlighted

[NEXT]
TODO: return graph with second outlier highlighted (sell)

[NEXT]
TODO: return graph with second outlier highlighted (buy back)

[NEXT]
show total profit made


[NEXT]
## 2. Stocks are Correlated

[NEXT]
TODO: positively correlated stock graph
![positive_corr_prices](images/positive_corr_prices.svg)

[NEXT]
TODO: negatively correlated stock graph
![negative_corr_prices](images/negative_corr_prices.svg)

[NEXT]
TODO: what these mean together


[NEXT SECTION]
## 2. Pure Python Implementation
![python](images/python.svg)

[NEXT]
### Short Term Strategy

Whenever we buy or borrow a stock...

...we only keep it for **one day**!

[NEXT]
### Trading Universe

Every day, we choose 3000 out of the 7000 stocks to trade.

Pick the 3000 most traded stocks.

This is our **trading universe**. We only ever trade these stocks.

[NEXT]
Every weekday just before the US stock market closes:

0. choose 3000 stocks to consider trading <!-- .element: class="hidden" -->
1. calculate each stock's daily returns for the past year  <!-- .element: class="hidden" -->
2. calculate correlation between each stock's returns <!-- .element: class="hidden" -->
3. use correlations and yesterday's returns to decide how much to buy/sell of each stock <!-- .element: class="hidden" -->
4. buy/sell decided stocks <!-- .element: class="hidden" -->
5. wait until tomorrow, then get rid of stocks bought/borrowed <!-- .element: class="hidden" -->

[NEXT]
Every weekday just before the US stock market closes:

0. choose 3000 stocks to consider trading <!-- .element: class="focus" -->
1. calculate each stock's daily returns for the past year  <!-- .element: class="hidden" -->
2. calculate correlation between each stock's returns <!-- .element: class="hidden" -->
3. use correlations and yesterday's returns to decide how much to buy/sell of each stock <!-- .element: class="hidden" -->
4. buy/sell decided stocks <!-- .element: class="hidden" -->
5. wait until tomorrow, then get rid of stocks bought/borrowed <!-- .element: class="hidden" -->

[NEXT]
Every weekday just before the US stock market closes:

0. choose 3000 stocks to consider trading <!-- .element: class="crossed" -->
1. calculate each stock's daily returns for the past year  <!-- .element: class="focus" -->
2. calculate correlation between each stock's returns <!-- .element: class="hidden" -->
3. use correlations and yesterday's returns to decide how much to buy/sell of each stock <!-- .element: class="hidden" -->
4. buy/sell decided stocks <!-- .element: class="hidden" -->
5. wait until tomorrow, then get rid of stocks bought/borrowed <!-- .element: class="hidden" -->

[NEXT]
Every weekday just before the US stock market closes:

0. choose 3000 stocks to consider trading <!-- .element: class="crossed" -->
1. calculate each stock's daily returns for the past year  <!-- .element: class="crossed" -->
2. calculate correlation between each stock's returns <!-- .element: class="focus" -->
3. use correlations and yesterday's returns to decide how much to buy/sell of each stock <!-- .element: class="hidden" -->
4. buy/sell decided stocks <!-- .element: class="hidden" -->
5. wait until tomorrow, then get rid of stocks bought/borrowed <!-- .element: class="hidden" -->

[NEXT]
Every weekday just before the US stock market closes:

0. choose 3000 stocks to consider trading <!-- .element: class="crossed" -->
1. calculate each stock's daily returns for the past year  <!-- .element: class="crossed" -->
2. calculate correlation between each stock's returns <!-- .element: class="crossed" -->
3. use correlations and yesterday's returns to decide how much to buy/sell of each stock <!-- .element: class="focus" -->
4. buy/sell decided stocks <!-- .element: class="hidden" -->
5. wait until tomorrow, then get rid of stocks bought/borrowed <!-- .element: class="hidden" -->

[NEXT]
Every weekday just before the US stock market closes:

0. choose 3000 stocks to consider trading <!-- .element: class="crossed" -->
1. calculate each stock's daily returns for the past year  <!-- .element: class="crossed" -->
2. calculate correlation between each stock's returns <!-- .element: class="crossed" -->
3. use correlations and yesterday's returns to decide how much to buy/sell of each stock <!-- .element: class="crossed" -->
4. buy/sell decided stocks <!-- .element: class="focus" -->
5. wait until tomorrow, then get rid of stocks bought/borrowed <!-- .element: class="hidden" -->

[NEXT]
Every weekday just before the US stock market closes:

0. choose 3000 stocks to consider trading <!-- .element: class="crossed" -->
1. calculate each stock's daily returns for the past year  <!-- .element: class="crossed" -->
2. calculate correlation between each stock's returns <!-- .element: class="crossed" -->
3. use correlations and yesterday's returns to decide how much to buy/sell of each stock <!-- .element: class="crossed" -->
4. buy/sell decided stocks <!-- .element: class="crossed" -->
5. wait until tomorrow, then get rid of stocks bought/borrowed <!-- .element: class="focus" -->

[NEXT]
TODO: refer back to AAPL example here for one day holdings

[NEXT]
### Simulation

Simulate how much money our trading algo would have made historically.

Use pricing data we already have to do this.

[NEXT]
### Simulation Date Range

|                |                    |
| -------------- | ------------------ |
| **Start Date** | 2nd January 1990   |
| **End Date**   | 10th November 2017 |

[NEXT]
### Calculating the Profits

TODO

[NEXT]
<!-- .slide: class="large-slide" -->
Let's write the strategy in

**Pure Python**.

[NEXT]
### Running the Code

```
> python3 -m test_strategy_purepython \
    --stock_price_dir data/stocks \
    --start_date 2000-01-02
    --end_date 2017-11-10
```

[NEXT]
## Profit

![pnl](images/pnl.svg)

[NEXT]
## Profit

|                                |                    |
| ------------------------------ | ------------------ |
| **Initial Investment**         | $TIME              |
| **Value at End of Simulation** | $TIME              |
| **Total Profit**               | $TIME              |
| **Return on Investment**       | %TIME              |

[NEXT]
### Success!
<span style="font-size: 120px">🎉</span>

[NEXT]
<!-- .slide: class="large-slide" -->
# Time Taken: 1 Month

![waiting_skeleton](images/waiting_skeleton.jpg)

_note_
TIME: fill in total time taken here

[NEXT]
<!-- .slide: class="large-slide" -->
# Bad for Research

**Very slow** to explore different trading strategies.

[NEXT]
<!-- .slide: class="large-slide" -->
# Bad for Production

Cannot run time-sensitive strategies that require real-time computation.

_note_
TODO: add note here to elaborate on example strategy


[NEXT]
<!-- .slide: class="large-slide" -->
What went wrong?

[NEXT]
<span class="highlighted">Three steps</span> are computationally heavy:

0. choose 3000 stocks to consider trading <!-- .element: class="crossed" -->
1. <span class="highlighted">calculate each stock's daily returns for the past year</span>
2. <span class="highlighted">calculate correlation between each stock's returns</span>
3. <span class="highlighted">use correlations and yesterday's returns to decide how much to buy/sell of each stock</span>
4. buy/sell decided stocks <!-- .element: class="crossed" -->
5. wait until tomorrow, then get rid of stocks bought/borrowed <!-- .element: class="crossed" -->

[NEXT]
<!-- .slide: class="hidden-table" -->
### Computationally Heavy Steps

Every day, these steps are run:

|        |                 |                                                        |
| ------ | --------------- | ------------------------------------------------------ |
| **1.** | **Returns**     | calculate each stock's daily returns for the past year |
| **2.** | **Correlation** | calculate correlation between each stock's returns     |
| **3.** | **Decision**    | use correlations and yesterday's returns to decide which stocks buy/sell |

[NEXT]
### Computationally Heavy Steps

Every day, these steps are run:

|        |                 |                                                        |
| ------ | --------------- | ------------------------------------------------------ |
| **1.** | **Returns**     | calculate each stock's daily returns for the past year |
| **2.** | **Correlation** | calculate correlation between each stock's returns     |
| **3.** | **Decision**    | use correlations and yesterday's returns to decide which stocks buy/sell |

[NEXT]
### How Much Computation is Required?

[NEXT]
| Step            | **Per Day** | **Full Simulation** |
| --------------- | ----------- | ------------------- |
| **Returns**     | TIME        | TIME                |
| **Correlation** | TIME        | TIME                |
| **Decision**    | TIME        | TIME                |

<div class="source">
  <p>
    <strong>operation</strong> is defined as an:
    <br />
    assignment, add, subtract, multiply, divide or comparison
  </p>
</div>

[NEXT]
<!-- .slide: class="large-slide" -->
## Total Operations

TIME

[NEXT]
## Trading Simulation
### Execution Time Breakdown

[NEXT]
**Total time:** TIME hours (TIME secs)

<div id="purepython-times"></div>

[NEXT]
<!-- .slide: class="large-slide" -->
Why is Python so slow?

_note_
Source for upcoming sections: https://jakevdp.github.io/blog/2014/05/09/why-python-is-slow/

[NEXT]
## Reason 1
### Dynamic Typing

[NEXT]
When a Python program executes, the interpreter doesn't know the type of the
variables that are defined.

![python_slow_1](images/python_slow_1.png)

[NEXT]
More instructions needed for any operation.

**Primary reason** Python is slower than C or other compiled languages
for processing numerical data.

[NEXT]
## Reason 2
### Interpreted, not Compiled

[NEXT]
Python code is interpreted at runtime.

Quick to iterate, but gives less chance to optimise.

During compilation, a smart compiler can look ahead and optimise inefficient code.

_note_
See section 5 to learn see how compiling Python code can dramatically speed up
code.

[NEXT]
## Reason 3
### Fragmented Memory Access

[NEXT]
![python_slow_2](images/python_slow_2.png)

[NEXT]
Bad for code that steps through **data in sequence**.

Iterate through a single list accesses completely different regions of memory.

Not **cache friendly**.


[NEXT SECTION]
## 3. Numpy
![numpy](images/numpy.svg)

[NEXT]
### The Foundation
Fundamental package for high performance computing in Python.

Many libraries/frameworks are built on top of NumPy.

[NEXT]
### Features

* multi-dimensional array objects
* routines for fast operations on arrays
  - mathematical, logical, sorting, selecting
* efficient loading/saving of numerical data to disk
  - including CSV

[NEXT]
`numpy.ndarray`

* class encapsulating n-dimensional arrays
* fixed size
* elements must be the same type

_note_
At the core of the NumPy package, is the ndarray object. This encapsulates
n-dimensional arrays of homogeneous data types, with many operations being
performed in compiled code for performance.

[NEXT]
## Examples

```python
import numpy as np
```
<!-- .element: class="large" -->

[NEXT]
### Creating an Array

```python
>>> a = np.arange(9, dtype=np.float64)
>>> a
array([0., 1., 2., 3., 4., 5., 6., 7., 8.])
>>> a.shape
(9,)
>>> a.strides
(8,)
```
<!-- .element: class="large" -->

[NEXT]
### Memory Layout
![ndarray](images/ndarray_1.svg)

_note_
A NumPy array in its simplest form is a Python object build around a C array.
That is, it has a pointer to a contiguous data buffer of values.

`data` is pointer indicating the memory address of the first byte in the array.

`dtype` indicates the type of elements stored in the array.

`shape` indicates the shape of the array. That is, it defines the dimensionality
of the data in the array and how many elements the array stores for each dimension.

The `strides` are the number of bytes that should be skipped in memory to go to the next element. If your strides are (32, 8), you need to proceed 8 bytes to get to the next column and 32 bytes to move to the next row.

`flags` is a set of configurable flags we don't need to cover here.

### Python View
![python_view](images/python_view.svg)

[NEXT]
### Reshape

```python
>>> b = a.reshape(3, 3)
>>> b
array([[0., 1., 2.],
       [3., 4., 5.],
       [6., 7., 8.]])
```

![ndarray](images/ndarray_2.svg)

[NEXT]
### Slicing One Dimension

```python
>>> b[:, :2]
array([[0., 1.],
       [3., 4.],
       [6., 7.]])
```

![ndarray](images/ndarray_4.svg)

[NEXT]
### Slicing Multiple Dimensions

```python
>>> b[:2, :2]
array([[0., 1.],
       [3., 4.]])
```

![ndarray](images/ndarray_5.svg)

[NEXT]
Reshaping or slicing arrays creates a **view**.

No copies are made.

[NEXT]
### Performance Benefits

* Data stored contiguously
  - no memory overhead
  - cache locality
* No copies for common reshaping/slicing operations
* Fast logical and mathematical operations
  - executed in heavily optimised compiled code

[NEXT]
### Benchmark
#### Adding 10,000,000 Numbers

[NEXT]
### Pure Python

```python
a = list(range(10000000))
b = list(range(10000000))

# 1. indexing
c = [a[i] + b[i] for i in range(len(a))]
```
<!-- .element: class="large" -->

[NEXT]
### NumPy

```python
import numpy as np

a = np.arange(10000000)
b = np.arange(10000000)

# 2. loop
c = np.zeros(len(a))
for i in range(len(a)):
    c[i] = a[i] + b[i]

# 3. built-in numpy addition operator
d = a + b
```
<!-- .element: class="large" -->

[NEXT]
### Timing (seconds)
<div id="basic-numpy-benchmark-times"></div>

[NEXT]
### Speedup Factor
<div id="basic-numpy-benchmark-speedup"></div>

[NEXT]
NumPy with loops is the slowest of all choices.

Takes **4x** longer than pure Python!

[NEXT]
### Explicitly Looping over Numpy Array
![numpy_add_loop](images/numpy_add_loop.svg)

_note_
For every integer, we're making two `__getitem__` calls, performing the
addition in Python and copying each result into the output numpy array with
a call to `__setitem__`.

This dramatically slows down the computation for two reasons:

1. This adds function call overhead. We invoke four Python functions for each
   integer. That's 40,000,000 function calls.
2. It performs three copies for each addition. It copies the `i`th element of
   `a` and `b`, then copies the addition into `c`.
3. The overhead and copies destroy cache locality. The copies are likely in a
   very different part of the address space, meaning the CPU is having to do
   more work to fetch data from RAM, instead of just using its local cache.

[NEXT]
### Using Built-in Addition
![numpy_add_native](images/numpy_add_native.svg)

_note_
The full addition logic is executed in native, compiled NumPy code. There are
no function call overheads and no copies.

The memory buffers storing `a` and `b` are directly accessed when adding.
Since those buffers are stored contiguously in memory, we're cache friendly.
The CPU has to fetch less data from RAM.

[NEXT]
### Keep it in NumPy!
Don't loop through `np.ndarray`s.

Move the computation to the NumPy/C/native code level where possible.

[NEXT]
### A Problem...
For arrays with the same size, operations are performed element-by-element.

Sometimes we want to apply smaller scalars or vectors to larger arrays.

_e.g. adding one to all elements in an array_

_note_
We want to use NumPy's built-in operations, but we don't want to perform loads of copies to match up the array sizes.

[NEXT]
### Adding 1 to an Array

![adding_one_to_array](images/adding_one_to_array.svg)

Adding 1 to **N** elements would take **N -1** copies!

[NEXT]
### Broadcasting
Allows us to apply smaller arrays to larger arrays.

**Without copying.**

[NEXT]
### Broadcasting Scalar to Array
![broadcasting](images/broadcasting_1d_0.svg)

[NEXT]
### Broadcasting Scalar to Array
![broadcasting](images/broadcasting_1d_1.svg)

[NEXT]
### Broadcasting Vector to Array
![broadcasting](images/broadcasting_2d_0.svg)

[NEXT]
### Broadcasting Vector to Array
![broadcasting](images/broadcasting_2d_1.svg)

[NEXT]
### Using NumPy for Trading Simulation

[NEXT]
### Recap

Every day, these steps are run:

|        |                 |                                                        |
| ------ | --------------- | ------------------------------------------------------ |
| **1.** | **Returns**     | calculate each stock's daily returns for the past year |
| **2.** | **Correlation** | calculate correlation between each stock's returns     |
| **3.** | **Decision**    | use correlations and yesterday's returns to decide which stocks buy/sell |

[NEXT]
### The First Step: Returns

Calculate each stock's daily returns for the past year.

[NEXT]
## Calculating Relative Return

Stock's relative daily return (in USD) on day _t_ is:

![equation](images/equation_returns.svg)

[NEXT]
## Example

| **Date**   | **AAPL Stock Price** |
| ---------- | -------------------- |
| 2017-08-01 | 148.92               |
| 2017-08-02 | 155.97               | 

<div>
  **What is AAPL's return at end of 2017-08-02?**
</div>
<!-- .element: style="font-size: 46px" class="fragment" data-fragment-index="0" -->
<div>
  **Return** = (155.97 - 148.92) / 148.92
</div>
<!-- .element: class="fragment" data-fragment-index="1" -->
<div>
  **Return** = 0.047
</div>
<!-- .element: class="fragment" data-fragment-index="2" -->
<div>
  **Return** = 4.7%
</div>
<!-- .element: class="fragment" data-fragment-index="3" -->

[NEXT]
<!-- .slide: class="large-slide" -->
Need to calculate return for all

stocks on all days.

[NEXT]
<!-- .slide: class="large-slide" -->
Could use a nested for loop:

<pre class="large"><code data-noescape class="python">returns = {}

for stock in stocks:
    for date in dates:
      todays_price = prices[stock, date]
      yesterdays_price = prices[stock, date - 1day]
      returns[stock] = (todays_price - yesterdays_price)
                       / yesterdays_price
</code></pre>

[NEXT]
<!-- .slide: class="large-slide" -->
Could use a nested for loop:

<pre class="large"><code data-noescape class="python"><mark>returns = {}</mark>

for stock in stocks:
    for date in dates:
      todays_price = prices[stock, date]
      yesterdays_price = prices[stock, date - 1day]
      returns[stock] = (todays_price - yesterdays_price)
                       / yesterdays_price
</code></pre>

[NEXT]
<!-- .slide: class="large-slide" -->
Could use a nested for loop:

<pre class="large"><code data-noescape class="python">returns = {}

<mark>for stock in stocks:</mark>
    for date in dates:
      todays_price = prices[stock, date]
      yesterdays_price = prices[stock, date - 1day]
      returns[stock] = (todays_price - yesterdays_price)
                       / yesterdays_price
</code></pre>

[NEXT]
<!-- .slide: class="large-slide" -->
Could use a nested for loop:

<pre class="large"><code data-noescape class="python">returns = {}

for stock in stocks:
    <mark>for date in dates:</mark>
      todays_price = prices[stock, date]
      yesterdays_price = prices[stock, date - 1day]
      returns[stock] = (todays_price - yesterdays_price)
                       / yesterdays_price
</code></pre>

[NEXT]
<!-- .slide: class="large-slide" -->
Could use a nested for loop:
<pre class="large"><code data-noescape class="python">returns = {}

for stock in stocks:
    for date in dates:
      <mark>todays_price = prices[stock, date]</mark>
      <mark>yesterdays_price = prices[stock, date - 1day]</mark>
      returns[stock] = (todays_price - yesterdays_price)
                       / yesterdays_price
</code></pre>

[NEXT]
<!-- .slide: class="large-slide" -->
Could use a nested for loop:
<pre class="large"><code data-noescape class="python">returns = {}

for stock in stocks:
    for date in dates:
      todays_price = prices[stock, date]
      yesterdays_price = prices[stock, date - 1 day]
      <mark>returns[stock] = (todays_price - yesterdays_price)</mark>
                       <mark>/ yesterdays_price</mark>
</code></pre>

[NEXT]
<!-- .slide: class="large-slide" -->
**Inefficent.**

Lots of copies and slow operations being run in Python code.

[NEXT]
<!-- .slide: class="large-slide" -->
**Using NumPy to compute returns:**

1. pack all stock prices for all dates into NumPy matrix <!-- .element: class="fragment" data-fragment-index="0" -->
2. perform bulk operations on matrix to keep computation in C <!-- .element: class="fragment" data-fragment-index="1" -->

[NEXT]
## Stock Price Matrix
![numpy_example_price_matrix](images/numpy_example_price_matrix.svg)

[NEXT]
## Stock Price Matrix
![numpy_example_price_matrix](images/numpy_example_price_matrix_marked.svg)

[NEXT]
## Stock Return Matrix
![numpy_example_price_matrix](images/numpy_example_returns_matrix_marked.svg)

[NEXT]
![numpy_example_returns_matrix_detail](images/numpy_example_returns_matrix_detail.svg)

[NEXT]
<!-- .slide: class="large-slide" -->
Instead of manually calculating each
cell one-by-one using Python loops...

[NEXT]
<!-- .slide: class="large-slide" -->
Use bulk matrix-based operations using NumPy.

[NEXT]
![numpy_example_returns_matrix_calc](images/numpy_example_returns_matrix_calc1.svg)

[NEXT]
### Shift Prices Forward One Day
![numpy_example_returns_matrix_calc](images/numpy_example_returns_matrix_calc2.svg)

[NEXT]
### Subtract 1-Day Shifted Price Matrix
<div style="height: 32px"></div>
![numpy_example_returns_matrix_calc](images/numpy_example_returns_matrix_calc3.svg)

[NEXT]
### Divide By 1-Day Shifted Price Matrix
<div style="height: 32px"></div>
![numpy_example_returns_matrix_calc](images/numpy_example_returns_matrix_calc4.svg)

[NEXT]
### Output
##### A Matrix With Each Stock's Daily Returns
<div style="height: 32px"></div>
![numpy_example_returns_matrix_calc](images/numpy_example_returns_matrix_calc5.svg)

[NEXT]
### Output
##### A Matrix With Each Stock's Daily Returns
![numpy_example_returns_matrix](images/numpy_example_returns_matrix.svg)

[NEXT]
# The NumPy Code

[NEXT]
<pre class="large"><code data-noescape class="python"># Construct empty date x symbol price matrix.
price_matrix = np.zeros(shape=(num_dates_in_sim,
                               num_stocks))

# ...populate price_matrix using CSV files...

# Calculate returns using matrix operations.
shifted_prices = np.roll(price_matrix, shift=1, axis=0)
shifted_prices[:1, :] = np.nan
returns = (price_matrix - shifted_prices)
          / shifted_prices  
</code></pre>

[NEXT]
<pre class="large"><code data-noescape class="python"># Construct empty date x symbol price matrix.
<mark>price_matrix = np.zeros(shape=(num_dates_in_sim,
                               num_stocks))</mark>

# ...populate price_matrix using CSV files...

# Calculate returns using matrix operations.
shifted_prices = np.roll(price_matrix, shift=1, axis=0)
shifted_prices[:1, :] = np.nan
returns = (price_matrix - shifted_prices)
          / shifted_prices  
</code></pre>

[NEXT]
<pre class="large"><code data-noescape class="python"># Construct empty date x symbol price matrix.
price_matrix = np.zeros(shape=(num_dates_in_sim,
                               num_stocks))

<mark># ...populate price_matrix using CSV files...</mark>

# Calculate returns using matrix operations.
shifted_prices = np.roll(price_matrix, shift=1, axis=0)
shifted_prices[:1, :] = np.nan
returns = (price_matrix - shifted_prices)
          / shifted_prices  
</code></pre>

[NEXT]
<pre class="large"><code data-noescape class="python"># Construct empty date x symbol price matrix.
price_matrix = np.zeros(shape=(num_dates_in_sim,
                               num_stocks))

# ...populate price_matrix using CSV files...

# Calculate returns using matrix operations.
<mark>shifted_prices = np.roll(price_matrix, shift=1, axis=0)</mark>
<mark>shifted_prices[:1, :] = np.nan</mark>
returns = (price_matrix - shifted_prices)
          / shifted_prices  
</code></pre>

[NEXT]
<pre class="large"><code data-noescape class="python"># Construct empty date x symbol price matrix.
price_matrix = np.zeros(shape=(num_dates_in_sim,
                               num_stocks))

# ...populate price_matrix using CSV files...

# Calculate returns using matrix operations.
shifted_prices = np.roll(price_matrix, shift=1, axis=0)
shifted_prices[:1, :] = np.nan
<mark>returns = (price_matrix - shifted_prices)</mark>
<mark>          / shifted_prices</mark>
</code></pre>

[NEXT]
## How The Returns Matrix is Used

Compute the returns matrix once at start of simulation.

Use slices of matrix for each date of sim. (**no copies!**)

Complete returns matrix is sized **7000 x 7000**.

[NEXT]
## Timings
#### Calculating All Returns
<div id="numpy-returns-times"></div>

[NEXT]
## Speedup
#### Calculating All Returns
<div id="numpy-returns-speedup"></div>

_note_
TIME: poplate these grapgs

[NEXT]
<!-- .slide: class="large-slide" -->
We use NumPy to perform similar optimisations for the **Correlation** and **Decision** steps.

[NEXT]
## Trading Simulation
### Execution Time Breakdown

[NEXT]
**Total time:** TIME hours ⟶ TIME hours

**Speedup:** TIMEx

<div id="numpy-times"></div>

[NEXT]
### Why NumPy is So Much Faster

* No extra memory overhead
* Minimal copying
* Cache friendly
* Operations executed in optimised compiled code

[NEXT]
But also...

[NEXT SECTION]
## 4. Vectorisation
![vectorisation](images/vectorisation.svg)

[NEXT]
> Process of converting an algorithm from operating on a **single** value at a
time to operating on a **set** of values at one time.

_note_
Source: https://software.intel.com/en-us/articles/vectorization-a-key-tool-to-improve-performance-on-modern-cpus

[NEXT]
Modern CPUs provide direct support for vector operations.

A **single instruction** is applied to **multiple** data points.

[NEXT]
### Adding Two Vectors
#### Single Instruction Single Data (SISD)

![sisd](images/sisd.svg)

Adding **_N_** numbers takes **_N_** instructions.

[NEXT]
### Adding Two Vectors
#### Single Instruction Multiple Data (SIMD)

![simd](images/simd.svg)

Adding **_N_** numbers takes **_N / 4_** instructions.

_note_
Basically for you as a coder, SIMD allows to perform four operations
(reading/writing/calculating) for the price of one instruction. The cost
reduction is enabled by vectorization and data-parallelism. You don’t even have
to handle threads and race conditions to gain this parallelism.

[NEXT]
### Example in C
#### Adding 10,000,000 Numbers

[NEXT]
### Non-Vectorised

```c
void add(float* a, float* b, float* out, int len) {
    for (int i = 0; i < len; ++i) {
        out[i] = a[i] + b[i];
    }
}
```

[NEXT]
### Vectorised

```c
void add_vectorised(float* a, float* b, float* out, int len) {
    int i = 0;
    for (; i < len - 4; i += 4) {
        out[i] = a[i] + b[i];
        out[i + 1] = a[i + 1] + b[i + 1];
        out[i + 2] = a[i + 2] + b[i + 2];
        out[i + 3] = a[i + 3] + b[i + 3];
    }
    for (; i < len; ++i) {
        out[i] = a[i] + b[i];
    }
}
```

[NEXT]
Disable optimisations to prevent compiler auto-vectorising.

```bash
clang -O0 vectorised_timings.c
```

[NEXT]
<!-- .slide: class="medium-slide" -->
**Speedup: 1.4x**
<div id="vectorise-benchmark"></div>

[NEXT]
### Vectorised Definitions

| **Context**     |                                                                                     |
| --------------- | ----------------------------------------------------------------------------------- |
| **Native Code** | Apply single operations to multiple data items at once using special CPU registers. |
| **Python**      | Keeping as much computation in `numpy`/native code as much as possible.             |

Both involve making algorithms use array/vector/matrix based computation (not iterative).

_note_
Vectorization describes the absence of any explicit looping, indexing, etc., in the code - these things are taking place, of course, just “behind the scenes” in optimized, pre-compiled C code. Vectorized code has many advantages, among which are:

* vectorized code is more concise and easier to read
* fewer lines of code generally means fewer bugs
* the code more closely resembles standard mathematical notation (making it easier, typically, to correctly code mathematical constructs)
* vectorization results in more “Pythonic” code. Without vectorization, our code would be littered with inefficient and difficult to read for loops.

[NEXT]
## Vectorisation for Trading Simulation

[NEXT]
<!-- .slide: class="large-slide" -->
We already got vectorisation for free.

[NEXT]
<!-- .slide: class="large-slide" -->
Using native NumPy operations often vectorises the code already.

[NEXT]
<!-- .slide: class="large-slide" -->
But not always...

[NEXT]
<!-- .slide: class="large-slide" -->
You might need to rewrite your algorithm.

This is **non-trivial**.

[NEXT]
<!-- .slide: class="large-slide" -->
Also...

[NEXT]
<!-- .slide: class="large-slide" -->
Not all algorithms are vectorisable.

[NEXT]
**The "Decision" step is still very slow.**

<div id="numpy-times-unvectorisable-highlighted"></div>


[NEXT SECTION]
## 5. Numba
![numba](images/numba.png)

_note_
see https://numba.pydata.org/ for examples

[NEXT]
<!-- .slide: class="large-slide" -->
Not all algorithms are vectorisable.

_note_
Are these non-vectorisable Python functions doomed to be slow?

[NEXT]
### Solution
Compile non-vectorisable Python code to native machine instructions.

[NEXT]
### Numba

Annotate Python functions with **decorators**.

Compiles them to optimised machine code at runtime.

**Just-in-time (JIT)** compilation.

**LLVM** for compiling to machine instructions.

_note_
Numba gives you the power to speed up your applications with high performance functions written directly in Python. With a few annotations, array-oriented and math-heavy Python code can be just-in-time compiled to native machine instructions, similar in performance to C, C++ and Fortran, without having to switch languages or Python interpreters.

[NEXT]
`numba.jit`

Decorator that tells Numba to compile a function to native instructions.

[NEXT]
### Example
#### Summing an Array of Numbers

```python
def sum_array(arr):
    result = 0
    for i in range(len(arr)):
        result += arr[i]
    return result
```
<!-- .element: class="large" -->

[NEXT]
### Sprinkle Some Numba Magic

<pre class="large"><code data-noescape class="python"><mark>from numba import jit</mark>

<mark>@jit(nopython=True)</mark>
def sum_array(arr):
    result = 0
    for i in range(len(arr)):
        result += arr[i]
    return result
</code></pre>

[NEXT]
### Timing (seconds)
<div id="numba-benchmark-times1"></div>

[NEXT]
### Speedup Factor
<div id="numba-benchmark-speedup1"></div>

[NEXT]
### Type Deduction

Numba automatically deduces the types of JIT-compiled functions.

Uses types of arguments in function's first invocation.

[NEXT]
### Explicitly Set Types

<pre class="large"><code data-noescape class="python">from numba import int64, jit

<mark>@jit(int64(int64[:]), nopython=True)</mark>
def sum_array(arr):
    result = 0
    for i in range(len(arr)):
        result += arr[i]
    return result
</code></pre>

[NEXT]
### Drawbacks

* Numba type inference sometimes fails
* You might need to specify types manually
  - arguably makes code more verbose / harder to read
* Restricted language features using `nopython=True`
  - variable types are fixed
  - cannot use arbitrary classes

_note_
Numba FAQ lists many of the drawbacks:
https://numba.pydata.org/numba-doc/dev/user/faq.html

[NEXT]
### Using Numba for Trading Simulation
Added `@jit(nopython=True)` to all functions.

Explicitly specified types.

[NEXT]
**Total time:** TIME mins ⟶ TIME mins

**Speedup:** TIMEx ⟶ TIMEx

<div id="numba-times"></div>

[NEXT]
### To Summarise
Use vectorised NumPy code where possible.

Fall back to Numba if code cannot be vectorised.


[NEXT SECTION]
## 6. The Final Timings
![final_timings](images/final_timings.svg)

[NEXT]
## Timing Summary
<div id="total-times"></div>

[NEXT]
## Speedup Summary
<div id="total-speedups"></div>

[NEXT]
TODO: add any extra optimisations here

[NEXT]
### Final Speedup
**1145** times faster.
<div id="total-speedups2"></div>

[NEXT]
## The Ultimate Goal
TODO

[NEXT]
### Detecting Outliers in the Full Dataset

TODO: scale

[NEXT]
<!-- .slide: class="large-slide" -->
**27 days** ⟶ **38 minutes**

[NEXT]
On a single Macbook pro.


[NEXT SECTION]
## Fin
![fin](images/fin.svg)

[NEXT]
Python is great for research.

Out of the box Python is **slow**.

[NEXT]
**Increasing demands for faster/real-time data processing.**

Processing large volumes of data or training complex machine learning models.

Standard Python in prod **isn't viable** for many use cases.

[NEXT]
Bad for **research**.

Very slow experimentation cycles.

[NEXT]
Bad for **production**.

Cannot run time-sensitive computational tasks.

[NEXT]
We can still use Python for research _and_ production.

By using Python's large ecosystem of scientific computing packages.

[NEXT]
Keep computation in **native code** as much possible.

**Vectorise** using NumPy where possible.

Use Numba to optimise **unvectorisable** code.

[NEXT]
<!-- .slide: class="large-slide" -->
If this isn't enough...

[NEXT]
<!-- .slide: class="large-slide" -->
Identify opportunities to **parallelise**.

[NEXT]
<!-- .slide: class="medium-slide" -->
Split computation into chunks that are processed in parallel.

Chunks can be processed by different **processes** or **machines**.

[NEXT]
<!-- .slide: class="large-slide" -->
Don't throw the problem to dev ops.

[NEXT]
<!-- .slide: class="large-slide" -->
Just using `numpy` and `numba`

alone can yield 1000x speedup.

[NEXT]
If RAM or disk is your bottleneck, parallelise using a cluster.

Otherwise, you can get **very** far with vectorisation and sprinkling
`@numba.jit` magic.


[NEXT]
<!-- .slide: class="large-slide" -->
**Спасибо!**

[NEXT]
<!-- .slide: class="small-slide" -->
### Links

* these slides:
  - http://donsoft.io/high-performance-data-processing-in-python
* example code from this talk:
  - https://github.com/DonaldWhyte/high-performance-data-processing-in-python/tree/master/code

[NEXT]
### Get In Touch

<div class="left-col" style="text-center: left">
  <br />
  [don@donsoft.io](mailto:don@donsoft.io)<br />
  [@donald_whyte](http://twitter.com/donald_whyte)<br />
  https://github.com/DonaldWhyte
</div>
<div class="right-col">
  ![small_portrait](images/donald.jpg)
</div>
<div class="clear-col"></div>


[NEXT SECTION]
## Appendix

[NEXT]
### References

**[1]** https://www.jetbrains.com/research/python-developers-survey-2017/

[NEXT]
### Timing Specifications
All performance timings in these slides were produced by running the code on a
machine with the following specs:

|                |                       |
| -------------- | --------------------- |
| **OS**         | macOS Sierra v10.12.6 |
| **Processor:** | 2.3 GHz Intel Core i5 |
| **Memory:**    | 8 GB 2133 MHz LPDDR3  |

[NEXT]
### Image Credits

* [Freepik](https://www.freepik.com/)
* [Icon Fonts](http://www.onlinewebfonts.com/icon)
* [Appzgear](https://www.flaticon.com/authors/appzgear)
