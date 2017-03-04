# PyOLab 

## Overview

The point of this project is to provide a suite of python routines that gives users complete control of an IOLab system, including examples of configuring the system and acquiring data. 

## CommonCode

This folder contains a collection of methods to allow the user to open a serial port, send commands to the IOLab hardware, and receive both status information and asynchronous data from the hardware:

* __commMethods.py__  
Communication with the IOLab hardware via the USB virtual com port. 
* __dataMethods.py__  
Focused on decoding and organizing the data received from the IOLab system.
* __iolabInfo.py__  
Code to provide callable information about the IOLab hardware & firmware (basically documentation). 
* __pyolabGlobals.py__  
Global structures and variables used to expose IOLab data and controls to the user. 
* __analClass.py__  
Used to separate the user code from the analysis code (basically a naive callback structure).

## user_example

This folder contains some example user code that imports and calls the PyOLab methods in CommonCode:

* __userExample.py__  
Example _main()_ code that opens the serial port, launches data fetching and data analysis threads, 
and then waits for user input.
* __userMethods.py__  
Example routines that are bound to the analysis thread in _main()_ and are called by the system during 
analysis to expose the user to acquired data.  
* __userGlobals.py__  
Example global user variables (may not be needed). 

## pyserial
PyOLab requires the pyserial module to handle com port communication. You can find more information at https://github.com/pyserial/pyserial/. 

Basic installation is easy: `pip install pyserial` should work for most users.

