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
Wealth of the tools!

TODO: icon cloud of stuffs

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

[NEXT SECTION]
## 2. Python Approach
![python](images/python.svg)

[NEXT]
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
How does it work? Basic primitives, memory layout, stride, etc.

[NEXT]
TODO: using numpy in naive way on dataset processing

[NEXT]
TODO: see massive speed increase from even some basic stuff!


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
## 5. Cython
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
