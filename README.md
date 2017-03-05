# PyOLab 

## Overview

The point of this project is to provide a suite of python routines that gives users complete control of an IOLab system. This archive contains a folder containing the PyOLab library code (__PyOLabCode__), two folders containing example user code (__HelloWorld__ and __DaqExample__), and a folder containing Documentation (__Documentation__). 

If you are new to Python you can get a great free release from [Anaconda](https://www.continuum.io/downloads). You will also need to get [PySerial](http://pyserial.readthedocs.io/en/latest/) (more info below). There is lots of online support and documentation for [learning Python](https://www.python.org/about/gettingstarted/). 

## PyOLabCode 

This folder contains a collection of methods to allow the user to open a serial port, send commands to the IOLab hardware, and receive both status information and asynchronous data from the hardware:

* __commMethods.py__  
Communication with the IOLab hardware via the USB virtual com port. 
* __setupMethods.py__  
Focused on setting up the IOLab system, initializing the 
threads to fetch and analyze data, and calling code to analyze these data..
* __dataMethods.py__  
Focused on decoding, organizing, and analyzing the data received from the IOLab system.
* __iolabInfo.py__  
Code to provide callable information about the IOLab hardware & firmware (basically documentation). 
* __pyolabGlobals.py__  
Global structures and variables used to expose IOLab data and controls to the user. 
* __analClass.py__  
Used to separate the user code from the analysis code (basically a naive callback structure).

---

## HelloWorld 

This folder contains the simplest possible user code example to talk to the system using the 
PyOLab library:

* __userExample.py__  
Very simple _main()_ code that opens the serial port, asks the 
dongle what its status is, receives the answer, and quits.

---

## DaqExample 

This folder contains a slightly more sophisticated user code example that uses the PyOLab 
library to implement a multi-threaded data acquisition system:

* __userExample.py__  
Example of some _main()_ code that opens the serial port, launches data fetching and data analysis threads, 
and then waits for user input.
* __userMethods.py__  
Examples of user routines that are bound to the analysis thread in _main()_ and are called by the system during 
analysis to expose the user to acquired data.  
* __userGlobals.py__  
Example of some global user variables used by the user methods (may not be needed by your code). 

---

## pyserial
PyOLab requires the __pyserial__ module to handle com port communication. You can find more information at https://github.com/pyserial/pyserial/. 

Basic installation of pyserial is straightforward: `pip install pyserial` should work for most users.

