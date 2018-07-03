### **Высокоэффективная обработка данных в Phyton**

#### High Performance Data Processing In Python

<p>
  <a href="http://twitter.com/donald_whyte">@donald_whyte</a>
</p>

<div id="logo-notice">
  <img src="images/pycon_russia.png" alt="pycon_russia" />
</div>

[NEXT]
### About Me

<div class="left-col1of3">
  ![small_portrait](images/donald.jpg)
</div>
<div class="right-col2of3" style="text-center: left">
  <div style="height: 27px"></div>
  <ul>
    <li>Software Engineer @ <strong>Engineers Gate</strong></li>
    <li>Scalable data infrastructure</li>
    <li>Real-time trading systems</li>
    <li>Python/C++/Rust developer</li>
  </ul>
</div>
<div class="clear-col"></div>

[NEXT]
### Motivation

TODO: Python great research tool. Easy to write, fast to iterate ideas?

[NEXT]
TODO: what about performance? Python is significantly slower than other
languages for computation!

[NEXT]
TODO: first basic graph of Python vs. C++

[NEXT]
TODO: second basic graph of Python vs. C++

[NEXT]
TODO: general purpose language, but also dominates a massive niche: data
processing and numerical computation

TODO: but why? it's so slow?

[NEXT]
### Wealth of Tools

![ecosystem](images/ecosystem.svg)

[NEXT]
### Outline

1. TODO: what we're doing with dataset
2. Process dataset in **pure Python**
3. Speed up processing using **numpy**
4. Speed up processing even more using **Cython**

[NEXT]
TODO: initial speed and end result

_X times speed up_


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
TODO: mention research question here

[NEXT]
### ISD-Lite

|                 |                          |
| --------------- | ------------------------ |
|**Dates**        | 1991-01-01 to 2011-12-31 |
|**Measurements** | 8                        |
|**Stations**     | ~30,000                  |
|**Rows**         | ~400,000,000             |

Approx one row per station every 6 hours.

_note_
Total stations: 29,630
Total rows: 391,908,528


[NEXT SECTION]
## 2. Let's use Python
![python](images/python.svg)

[NEXT]
### Data Format
TODO: how to implement processing

[NEXT]
TODO: really slow!

[NEXT]
TODO: what is Python actually doing under the hood to make it so slow?


[NEXT SECTION]
## 3. Numpy
![numpy](images/numpy.svg)

[NEXT]
what is it?

[NEXT]
How does it work? Basic primitives, memory layout, stride, etc.]

[NEXT]
### `numpy.ndarray`

TODO: summary of why it is (one or many D array of contiguous memory that stores data)

[NEXT]
### `numpy.ndarray`

| | |
| - | - |
| `data` | pointer indicating the memory address of the first byte in the array |
| `dtype` | the kind of elements contained within the array |
| `shape` | TODO |
| `stride` | TODO |
| `flags` | TODO |

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
## 5. cython
![cython](images/cython.svg)

_note_
see https://cython.readthedocs.io/en/latest/src/tutorial/numpy.html for examples

[NEXT]
TODO: what is cython

[NEXT]
DSL on top of Python that annotates the code with static code±!

[NExT}]
massive optimisations, just by using on

[NEXT]
TODO: show graph of speed with and without cython

[NEXT]
works especially well with numpy, show how

[NEXT]
TODO: show graph of speed with and without cython numpy code

[NEXT SECTION]
## Fin
![fin](images/fin.svg)

[NEXT]
TODO: show final graphs on log scale of speeds

[NEXT]
TODO: conclusion

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
### Image Credits

[Freepik](https://www.freepik.com/)
