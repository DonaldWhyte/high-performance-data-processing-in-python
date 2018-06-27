# Mocking in Rust using Double

### [View Presentation Slides](http://donaldwhyte.github.io/mocking-in-rust-using-double/)

Talk demonstrating how to write behaviour verification tests in Rust using mocks.

Topics covered:

* unit testing in Rust
* behaviour verification with test doubles
* mocking in Rust tests using the [*`double`*](https://github.com/DonaldWhyte/double) crate

## Running Presentation

You can also run the presentation on a local web server. Clone this repository and run the presentation like so:

```
npm install
grunt serve
```

The presentation can now be accessed on `localhost:8080`. Note that this web application is configured to bind to hostname `0.0.0.0`, which means that once the Grunt server is running, it will be accessible from external hosts as well (using the current host's public IP address).
