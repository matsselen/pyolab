# PyOLab 

## Overview

The point of this project is to provide a suite of python routines that gives users complete control of an IOLab system, including examples of configuring the system and acquiring data. The are three main folders in this archive: __CommonCode__, __Example__, and __Documentation__

## CommonCode

This folder contains a collection of methods to allow the user to open a serial port, send commands to the IOLab hardware, and receive both status information and asynchronous data from the hardware:

<<<<<<< Updated upstream
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

---

## Example

This folder contains some example user code that imports and calls the PyOLab methods in CommonCode:

* __userExample.py__  
Example of some _main()_ code that opens the serial port, launches data fetching and data analysis threads, 
and then waits for user input.
* __userMethods.py__  
Examples of user routines that are bound to the analysis thread in _main()_ and are called by the system during 
analysis to expose the user to acquired data.  
* __userGlobals.py__  
Example of some global user variables used by the user methods (may not be needed by your code). 

---
=======
* ___commMethods.py___ Communication with the IOLab hardware via the USB virtual com port. 
* dataMethods.py
* iolabInfo.py
* pyolabGlobals.py
* analClass.py

>>>>>>> Stashed changes

## pyserial
PyOLab requires the pyserial module to handle com port communication. You can find more information at https://github.com/pyserial/pyserial/. 

Basic installation is easy: `pip install pyserial` should work for most users.

