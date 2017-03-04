# PyOLab 

## Overview

The point of this project is to provide a suite of python routines that gives users complete control of an IOLab system, including examples of configuring the system and acquiring data. 

## CommonCode

This folder contains a collection of methods to allow the user to open a serial port, send commands to the IOLab hardware, and receive both status information and asynchronous data from the hardware:

* __commMethods.py__ Communication with the IOLab hardware via the USB virtual com port. 
* dataMethods.py
* iolabInfo.py
* pyolabGlobals.py
* analClass.py


## pyserial
PyOLab requires the pyserial module to handle com port communication. You can find more information at https://github.com/pyserial/pyserial/. 

Basic installation is easy: `pip install pyserial` should work for most users.

