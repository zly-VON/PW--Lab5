# Lab 5 - go2web CLI

This laboratory implements a command line program that allows users to make HTTP requests to URLs or search terms using a search engine.

### CLI

The program implements the following CLI:
```
  go2web -u <URL>         # make an HTTP request to the specified URL and print the response
  go2web -s <search-term> # make an HTTP request to search the term using your favorite search engine and print top 10 results
  go2web -h               # show this help
  ```

### Task

- Executable with `-h`, `-u` and `-s` options

### Tasks for Extra Points

- results/links from search engine can be accessed (using your CLI)
- implementation of an HTTP cache mechanism

### Live Demo
![Alt Text](assets/live_demo.gif)