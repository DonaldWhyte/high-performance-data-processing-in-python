# High Performance Data Processing in Python

### [View Presentation Slides](http://donaldwhyte.github.io/high-performance-data-processing-in-python)

Talk demonstrating how to massively optimise data processing and numerical computation in Python. We perform outlier detection on a large time-series weather dataset ([ISD](https://www.ncdc.noaa.gov/isd)). We take detecting outliers in 600GBs worth of data in Python down from 28 days to 38 minutes.

Topics covered:

* motivations for fast numerical processing in Python
* why Python is a slow programming language
* fast numerical processing in `numpy`
* vectorisation
* using `numba` to optimise non-vectorised code
* parallelising computation using `joblib`

## Running Presentation

You can also run the presentation on a local web server. Clone this repository and run the presentation like so:

```
npm install
grunt serve
```

The presentation can now be accessed on `localhost:8080`. Note that this web application is configured to bind to hostname `0.0.0.0`, which means that once the Grunt server is running, it will be accessible from external hosts as well (using the current host's public IP address).
