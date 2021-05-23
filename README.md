# MSCS710 - WAR (Windows Analysis Reporting)
> A computer metrics collector and data compiler for Windows machines using Python.
> All components are subject to change as the project continues.

## Table of contents
* [General info](#general-info)
* [Requirements](#requirements)
* [How to run](#how-to-run)
* [Computer Metric Collector](#computer-metric-collector)
* [UI](#ui)
* [Pipeline](#pipeline)
* [Testing](#testing)
* [Deployment](#deployment)

## General Info
WAR is a software service that gathers system resource utilization information on multiple host machines and to persist on a centralized database. The purpose of WAR is to allow the users to visualize the system resource utilization of their machines.

WAR collects computer metrics on one or more client machines. After collection, the computer metrics will persist in a database. Using the metrics collected, WAR will generate user friendly reports for the users to analyze the performance of each of their machines. 

Video about WAR: 
https://www.youtube.com/watch?v=5LYybF8Kr9E

Design Document: 
https://docs.google.com/document/d/1CenpGOayQFXi0Al1QuUOC-ZHtPxEydIBZ76IOM_xA2U/

Code Review:
https://youtu.be/s8xK9idr6kA


## Requirements
#### Computer Metrics Collector Libraries
 1) pycryptodomex==3.10.1
 1) requests==2.25.1
 1) psutil==5.8.0
 1) py-cpuinfo==7.0.0
 1) panda==1.2.3
 1) pyinstaller==4.3

## How to Run

In order to start up Computer Metric Collector, please execute the following from the root directory:
1) Download or Clone the repository
```
git clone https://github.com/tfedoris/MSCS_710_Software_Project.git
```
1) Launch the command line terminal
1) Move to the Computer Metrics Collector
1) Install dependent libraries from requirements.txt
```
pip3 install -r computerMetricCollector/requirements.txt
```

Choose a one of the method to start the collector
1) Run from python shell
```
python computerMetricCollector/__init__.py
```

1) If you only want the script to run onnce for testing purposes, execute the following:

```
python -m computerMetricCollector.__init__ -t True
```
1) Create executable to run the Computer Metrics Collector
    1) Open a command line terminal in the project
    1) Create the executable with pyinstaller
```
pyinstaller --onefile --name ComputerMetricsCollector --distpath ./computerMetricCollector/dist computerMetricCollector\__init__.py
```
Pyinstaller will create an executable named `ComputerMetricsCollector.exe` in `computerMetricCollector/dist/` folder.

After starting the collector, the spawned window will prompt the user for registration ID that is associated with their account.
> User need to register a account in https://www.wardashboard.com/ to obtain a registration ID

Once the script is running, you should be able to view your computer metrics here: https://www.wardashboard.com/

## Computer Metric Collector
The Computer Metric Collector is a python program for collecting computer performance data from the host computer and peristing those data to the remote database for users the visual their computers' performance.
When start, a window will prompt to request user to input their registration ID if the ID is not already passed as argument. 
After the registration ID is read, the program will start collecting computer performance data. 
It will collect data continuously until the user stop the program. 
Every collection will be output to the windows to user to visualize. 

## UI
The website is hosted on an AWS EC2 instance, deployed using AWS Amplify. AWS Amplify provides a free web service for us to develop the website with flexibility and automatic deployment through GitHub. We do not need to create a web server
machine to host the website server. For the user interface, we will be utilizing React and Typescript to design a single page application to visualize the metrics. The application has been integrated with Amazon's authentication services utilizing
their cognito user pools. Through this service, users can register for an account and have their credentials stored securiely on Amazon's web servers. Once a user has created an account, they will be provided with a Registration ID to be used with the 
metrics collector application running on their local machine. This registration ID will link their machine with their account so they can view visualized metrics collected from their system. Recharts is an open-source graphing library that powers the 
data visualization for this application. We will use this library to display the data that is extracted from the database.

To get started with creating an account, you can visit the WAR Dashboard web application here: https://wardashboard.com

## Database
The database that stores the computer metrics collection from client machines is in MySQL. We choose MySQL for its compatibility with Amazon RDS and AWS's API Gateway that utlizes Lambda Functions.

## Pipeline
The pipeline we are using is a Jenkins server running on a Windows 10 machine EC2 instance. The script for the pipeline can be found in the Jenkinsfile. While it is preferable and possible to run the pipeline script automatically with polling for new commits, at the moment we do it manually since there is only so much processing that can be done on the free tier of our EC2 instance. If we were to upgrade our machine, it would no longer give us the not enough free space error if there are multiple commits occurring at similar times.

The build system can be accessed here: http://52.27.174.67:8080/

Build System Video: https://www.youtube.com/watch?v=SpIvcscqmTM

## Testing
Our test approach document can be found here: https://docs.google.com/document/d/1jBDfno7a5ibr6q27d9NrudaH47j9lbALaEbSCyMYlCo/edit?usp=sharing

In order to run the test suites, please execute the following from the root directory:

```
python -m computerMetricCollector/test/__init__.py
```

Videos of the tests can be seen here:
https://www.youtube.com/watch?v=ZYbLcZmTDVA "Part 1"
https://www.youtube.com/watch?v=bn93DpB0jCU "Part 2"

## Deployment
The ComputerMetricsCollector.exe created in the instructions on how to run the program is the final deliverable to be given to users but it must stay in the same file structure.
It can be distributed a number of ways so long as the users can download the folder.
The users have to do the following steps:
 1) Download folder from distribution site chosen. Example is found here: https://www.dropbox.com/sh/c3ihjkq7pe6laqe/AAA0A27P93v_egKAR4ijDW6ea?dl=0
 2) Register on https://www.wardashboard.com/
 3) Run ComputerMetricsCollector.exe using the registration code given on https://www.wardashboard.com/ under the "Account" tab
 4) Look at the metrics on https://www.wardashboard.com/ under the "Dashboard" tab

## Credits
Windows Analysis Reporting created by Timothy Hoang, Tyler Fedoris, and Yi Lin
