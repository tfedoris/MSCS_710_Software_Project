# MSCS710 - WAR (Windows Analysis Reporting)
> A computer metrics collector and data compiler for Windows machines using Python.

## Table of contents
* [General info](#general-info)
* [Requirements](#requirements)
* [How to run](#how-to-run)
* [Metric Collector](#metric-collector)
* [UI](#ui)
* [Pipeline](#pipeline)
* [Testing] (#testing)

## General Info
WAR is a software service that gathers system resource utilization information on multiple host machines and to persist on a centralized database. The purpose of WAR is to allow the users to visualize the system resource utilization of their machines.

WAR collects computer metrics on one or more client machines. After collection, the computer metrics will persist in a database. Using the metrics collected, WAR will generate user friendly reports for the users to analyze the performance of each of their machines. 

Video about WAR: 
(https://www.youtube.com/watch?v=5LYybF8Kr9E)

Design Document: 
(https://docs.google.com/document/d/1CenpGOayQFXi0Al1QuUOC-ZHtPxEydIBZ76IOM_xA2U/)


## Requirements
#### Computer Metrics Collector Libraries
 1) pycryptodomex 3.10.1
 1) requests 2.25.1
 1) psutil 5.8.0
 1) py-cpuinfo 7.0.0
 1) pandas 1.2.3

## How to Run
In order to start up war, please execute the following from the root directory:

```
pip3 install -r computerMetricCollector/requirements.txt
python computerMetricCollector/__init__.py
```
If you only want the script to run onnce for testing purposes, execute the following:
```
python -m computerMetricCollector.__init__ -t True
```

Once the script is runnnning, you should be able to view your computer metrics here
(https://www.wardashboard.com/)

## Metric Collector

## UI
The website is hosted on an Amazon EC2 server using Apache. EC2 server provides a free web service for us to develop the website with flexibility. We do not need to create a web server machine to host the website server. For the user interface, we will be utilized Flask to design the website. Flask is a WSGI (Web Server Gateway Interface) web framework. Using Flask, we developed a model-view-controller architecture for our website. We set up routes that will generate graphs using Plotly. Plotly is an open-source graphing library that can be found [here][1]. We will use this library to display the data that is extracted from the database. The routes will also serve web pages which are HTML files that were generated using Jinja.

[1]: plotly.com/python/

## Database
The database that stores the computer metrics collection from client machines is in MySQL. We choose MySQL for its compatibility with Amazon RDS and Apache web server. 

## Pipeline
The build system can be accessed here:
(http://52.27.174.67:8080/)

Build System Video:
(https://www.youtube.com/watch?v=SpIvcscqmTM)

## Testing
Our test approach documennt can be found here:
(https://docs.google.com/document/d/1jBDfno7a5ibr6q27d9NrudaH47j9lbALaEbSCyMYlCo/edit?usp=sharing)

In order to run the test suites, please execute the following from the root directory:

```
python -m computerMetricCollector/test/__init__.py
```

Videos of the tests can be seen here:
(https://www.youtube.com/watch?v=ZYbLcZmTDVA "Part 1")
(https://www.youtube.com/watch?v=bn93DpB0jCU "Part 2")

## Credits
Windows Analysis Reporting created by Timothy Hoang, Tyler Fedoris, and Yi Lin
