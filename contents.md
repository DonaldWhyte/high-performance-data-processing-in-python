<!-- .slide: data-background="images/intro_background.png" class="background" -->
### **Высокоэффективная обработка данных в Phyton**

#### High Performance Data Processing In Python

<p>
  <a href="http://twitter.com/donald_whyte">@donald_whyte</a>
</p>

<div id="logo-notice">
  <img src="images/pycon_russia.png" alt="pycon_russia" />
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
TODO: three obvious reasons

TODO

TODO

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background large-slide" -->
**What about production?**

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->

TODO: data analysis used to be the realm of research --
one-off jobs to produce papers or presentations

TODO: with ML being bigger than ever, actually _running_

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->

### The Traditional Process

1. Researcher builds model in their tech of choice
2. Programmer takes research code and rewrites it
3. Production code is deployed
4. Everything works fine

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
### Success!
![cheering](images/cheering.gif)

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
### The Reality...
![bad_times](images/bad_times.gif)

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
### The Reality...
1. Researcher builds model that works on their machine
2. Programmer TODO
3. TODO
4. Deployment is delayed
5. Cut backs TODO

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
### A Better Process
Research and production code is **identical**.

_note_
A better process is to make the research and production code **identical**.
They can be configured differently, but the code which pre-processes the data,
builds the model and TODO should be the same.

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background large-slide" -->
What about performance?

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
## TODO 1
<div id="python-vs-c-chart1"></div>

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
## TODO 2
<div id="python-vs-c-chart2"></div>

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
## TODO 3
<div id="python-vs-c-chart3"></div>

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
### Reasons Python is Slow
* TODO
* TODO
* TODO

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
Why do people still use Python in production?

[NEXT]
<!-- .slide: data-background="images/ecosystem.png" class="background" -->
# Ecosystem

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
### NumPy

<div class="left-col">
  <ul>
  <li>Heart of TODO.</li>
  <li>TODO</li>
  <li>TODO</li>
  </ul>
</div>
<div class="right-col">
  <img src="images/numpy_coloured.svg" alt="numpy_coloured" />
</div>
<div class="clear-col"></div>

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
TODO: focus of tlak

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background" -->
### Outline

1. Analyse a large weather dataset
2. Process dataset in **pure Python**
3. Speed up processing using **NumPy** and vectorisation
4. Speed up processing even more using **Numba**

[NEXT]
<!-- .slide: data-background="images/intro_background.png" class="background large-slide" -->
## Final Optimised Solution?

**1000 times** faster.


[NEXT SECTION]
## 1. The Dataset
![dataset](images/dataset.svg)

[NEXT]
### Integrated Surface Database (ISD)

![isd](images/isd.gif)

_note_
Global database of atmospheric data.

This map shows the spatial distribution of Integrated Surface Database
stations for all time periods.

Source: https://www.ncdc.noaa.gov/isd

[NEXT]
## Measurements

<div class="left-col" style="text-center: center;">
  <p>wind speed and direction</p>
  <p>temperature</p>
  <p>sea level pressure</p>
  <p>sky visibility</p>
</div>
<div class="right-col">
  <img src="images/weather_measurements.svg" alt="weather_measurements" />
</div>
<div class="clear-col"></div>

_note_
Detailed list of fields:

wind speed and direction, wind gust, temperature, dew point, cloud data, sea level pressure, altimeter setting, station pressure, present weather, visibility, precipitation amounts for various time periods, snow depth, and various other elements as observed by each station.

[NEXT]
## Coverage

<div class="left-col">
  <img src="images/globe.svg" alt="globe" />
</div>
<div class="right-col" style="text-center: left; padding-top: 12px">
  <p>7 continents</p>
  <p>35,000 weather stations</p>
  <p>1901 to now</p>
  <p>from over 100 data sources</p>
</div>
<div class="clear-col"></div>

[NEXT]
<!-- .slide: class="large-slide" -->
**Total Data Volume > 600GB**

_note_
ISD integrates data from over 100 original data sources, including numerous data formats that were key-entered from paper forms during the 1950s–1970s time frame

[NEXT]
### Example
![tabriz_airport](images/tabriz_airport.png)

[NEXT]
| **timestamp**       | **station_id** | **wind_speed_rate** | *...* |
| ------------------- | -------------- | ------------------- | ----- |
| 1995-01-06 03:00:00 | 407060         | 50.0                | ...   |
| 1995-01-06 06:00:00 | 407060         | 70.0                | ...   |
| 1995-01-06 09:00:00 | 407060         | null                | ...   |
| 1995-01-06 12:00:00 | 407060         | 60.0                | ...   |
| 1995-01-06 16:00:00 | 407060         | 20.0                | ...   |

_note_
TODO: add explanation of wind speed rate here

[NEXT]
### Tabriz Wind Speed Rate
##### (2011-12-29 to 2011-12-31)
![tabriz_wind_speed_rate](images/tabriz_wind_speed_rate.png)

[NEXT]
# Goal
TODO: mention research question here

[NEXT]
### Trimmed Data

**ISD-Lite Dataset**

|                 |                          |
| --------------- | ------------------------ |
|**Dates**        | 1991-01-01 to 2011-12-31 |
|**Measurement**  | Wind Speed Rate          |
|**Stations**     | ~6000                    |
|**Rows**         | ~400,000,000             |

_note_
Total stations: 29,630
Total rows: 391,908,527


[NEXT SECTION]
## 2. Let's Use Python
![python](images/python.svg)

[NEXT]
How do we detect hurricanes?

Finding data points with unusually low/high `wind_speed_rate` values.,

[NEXT]
### Detecting Outliers
![outlier_detection](images/outlier_detection.png)

[NEXT]
### Detecting Outliers

At each point `i` in the time series:

1. Take values in time series between points `i - 30` and `i`
2. Calculate mean and standard deviation
3. Value at `i` is an outlier if it's:
  - more than **6 standard deviations** away from the mean

[NEXT]
![rolling_mean_and_std](images/rolling_mean_and_std.png)

[NEXT]
### Problem: Null Values
<table>
  <tr>
    <th>timestamp</th>
    <th>station_id</th>
    <th>wind_speed_rate</th>
  </tr>
  <tr><td>1995-01-06 03:00:00</td><td>407060</td><td>50.0</td></tr>
  <tr><td>1995-01-06 06:00:00</td><td>407060</td><td>70.0</td></tr>
  <tr class="bad-row"><td>1995-01-06 09:00:00</td><td>407060</td><td>null</td></tr>
  <tr><td>1995-01-06 12:00:00</td><td>407060</td><td>70.0</td></tr>
  <tr><td>1995-01-06 17:00:00</td><td>407060</td><td>20.0</td></tr>
</table>

[NEXT]
### Solution: Fill Forward
<table>
  <tr>
    <th>timestamp</th>
    <th>station_id</th>
    <th>wind_speed_rate</th>
  </tr>
  <tr><td>1995-01-06 03:00:00</td><td>407060</td><td>50.0</td></tr>
  <tr><td>1995-01-06 06:00:00</td><td>407060</td><td>70.0</td></tr>
  <tr class="good-row"><td>1995-01-06 09:00:00</td><td>407060</td><td>70.0</td></tr>
  <tr><td>1995-01-06 12:00:00</td><td>407060</td><td>70.0</td></tr>
  <tr><td>1995-01-06 17:00:00</td><td>407060</td><td>20.0</td></tr>
</table>

[NEXT]
### Complete Process
TODO: add diagram illustrating full process

_note_
1. Split full dataset into separate station time series
2. For each weather station time series, detect outliers by:
  1. calculate rolling mean and stdev at each point
  2. check if a point is > 6 stdevs away from its rolling mean value
  3. if so, mark point as outlier
3. generate CSV containing all outliers in each station's data

[NEXT]
### Input

* HDF5 file containing three columns:
  - `timestamp`
  - `station_id`
  - `wind_speed_rate`
* Rows already sorted by station and time

_note_
TODO: what is HDF5 file

[NEXT]
### The Code
TODO: point to where you can find the code

[NEXT]
```bash
> python3 -m find_outliers_purepy \
    --input isdlite.hdf5 \
    --output outliers.csv \
    --measurement wind_speed_rate
Found TODO outliers in TODO stations
Outlier search took TODO
```

[NEXT]
```bash
> cat outliers.csv | head
TODO
```

[NEXT]
TODO: show news report of actual incident

[NEXT]
### Performance
* **Time taken:** TODO
* **Average time per row:** TODO

[NEXT]
### Profiling the Code

Let's find out which step(s) were the performance bottlenecks.

```bash
> python3 -m cProfile -o profile_output \
     find_outliers_purepy.py \
     --input isdlite.hdf5 \
     --output outliers.csv \
     --measurement wind_speed_rate
```

[NEXT]
### Visualising Performance Bottlenecks

```bash
> pip3 install snakeviz
> snakeviz profile_output
```

[NEXT]
TODO: show snakeviz output

[NEXT]
TODO: break down time for each step (bar chart, standard graph for all breakdowns)

[NEXT]
TODO: what is Python actually doing under the hood to make it so slow?

[NEXT]
### Reason 1: Memory Indirection
TODO

[NEXT]
### Reason 2: Difficult to Vectorise
TODO


[NEXT SECTION]
## 3. Numpy
![numpy](images/numpy.svg)

[NEXT]
Fundamental package for high performance computing in Python.

[NEXT]
### The Foundation

Foundation on which nearly all of the higher-level data tools are built.

Example tools:

* TODO

[NEXT]
### Features

* `ndarray`, a fast and space-efficient multidimensional array
  - provides vectorized arithmetic operations and sophisticated broadcasting capabilities

[NEXT]
How does it work? Basic primitives, memory layout, stride, etc.

[NEXT]
### `numpy.ndarray`

TODO: summary of why it is (one or many D array of contiguous memory that stores data)

[NEXT]
### `numpy.ndarray`

|          |                                                                      |
| -------- | -------------------------------------------------------------------- |
| `data`   | pointer indicating the memory address of the first byte in the array |
| `dtype`  | the kind of elements contained within the array                      |
| `shape`  | TODO |
| `stride` | TODO |
| `flags`  | TODO |

_note_
The shape indicates the shape of the array

The strides are the number of bytes that should be skipped in memory to go to the next element. If your strides are (10,1), you need to proceed one byte to get to the next column and 10 bytes to locate the next row.

[NEXT]
TODO: given visual example of shape (3,0)

[NEXT]
TODO: given visual example of shape (0, 3)

[NEXT]
TODO: given visual example of shape (3, 3)

[NEXT]
TODO: given visual example of shape (4, 2)

[NEXT]
TODO: show reshaping, and how it works without copying and just changing the stride

[NEXT]
TODO: transpose example, which is a common use case for reshaping

[NEXT]
TODO: broadcasting -- can reduce copies

[NEXT]
TODO: using numpy in naive way on dataset processing

[NEXT]
TODO: use it to perform processing, massive speed increase for even some basic stuff!


[NEXT SECTION]
## 4. Vectorisation
![vectorisation](images/vectorisation.svg)

[NEXT]
TODO: why does numpy provide such a speedup?

[NEXT]
TODO: memory efficiency, packed together, less indirection in memory,
helps cache lines, lower level/less instructions

[NEXT]
TODO: but also vectorisation! explain what this is

[NEXT]
TODO: give high-level theoretical example of vectorisation

[NEXT]
TODO: achieved via SIMD -- show CPU register example

[NEXT]
TODO: show basic toy example with timings

[NEXT]
TODO: show numpy code from the example and how it's vectorising

[NEXT]
TODO: graph to recap non-vectorised and vectorised

[NEXT]
TODO: show how you can even improve vectorisation via memory efficiency!

[NEXT]
TODO: another graph to demonstrate speedup

[NEXT]
But wait...there's more!


[NEXT SECTION]
## 5. Numba
![numba](images/numba.png)

_note_
see https://cython.readthedocs.io/en/latest/src/tutorial/numpy.html for examples

[NEXT]
TODO: what is numba

[NEXT]
potentially massive optimisations with a couple of line of code

[NEXT]
TODO: show JIT decorator

[NEXT]
TODO: show what types it deduces under the hood

[NEXT]
TODO: show graph of speed with and without Numba

[NEXT]
TODO: emphasise that it won't really speed up vectorised numpy code

TODO: but it's good optimising the inherent loops present

[NEXT SECTION]
## Fin
![fin](images/fin.svg)

[NEXT]
TODO: show final graphs on log scale of speeds

[NEXT]
TODO: conclusion

[NEXT]
TODO: be sure to emphasise the importance of numerical computation optimisation

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
### Image Credits

[Freepik](https://www.freepik.com/)
