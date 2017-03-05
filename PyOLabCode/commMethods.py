# system stuff
import time
import serial
import serial.tools.list_ports
from threading import Thread

# local stuff
from pyolabGlobals import G


"""
This file contains a set of methods that allows a user to communicate 
with the IOLab system via the virtual com port. 

"""

#======================================
# Returns a list of names of the serial ports that
# the OS thinks has an IOLab dongle is plugged into them
def getIOLabPortName():

    # get a list of all serial ports
    ports = list(serial.tools.list_ports.comports())
    
    # loop over all of the ports found and get the name of 
    # the last one that is an IOLab USB virtual com port
    
    p = ''
    pList = []
    for port in ports:
         pInfo = list(port)
         if 'IOLab USB Dongle' in pInfo[1]:
            pList.append(pInfo)

    nFound = len(pList)

    if nFound == 0:
        print "Found no IOLab USB Dongles"
    
    else:

        p = pList[0][0]
        if nFound == 1:
            print "Found IOLab USB Dongle: " + p
        else:
            print "Warning: found " +str(nFound)+ " IOLab USB Dongles."
            print "Using the first one found: " + p

    return p

#======================================
# Opens the IOLab com port that has name pName
#
def openIOLabPort(pName):

    # open the com port
    serialport = serial.Serial(pName)
    serialport.baudrate = 115200
    serialport.timeout  = 1

    return serialport


#=======================================================================
# This next bunch of routines sends commands to the IOLab remote via
# the serial port "s". For a description of the data packets that are returned
# by each one see the USB Interface Specification document 
# (Indesign document number 1814F03 Revision 11, available on the IOLab web page at
#  http://www.iolab.science/Documents/IOLab_Expert_Docs/IOLab_usb_interface_specs.pdf)

#======================================
# Ask the dongle to send a data packet of type 0x14 telling us its status
def getDongleStatus(s):

    command = [0x02, 0x14, 0x00, 0x0A] 
    s.write(bytearray(command))
    time.sleep(G.sleepCommand)  #give the serial port some time to receive the data

#======================================
# Ask remote to send a data packet of type 0x2a telling us its status
def getRemoteStatus(s, remote):

    command = [0x02, 0x2A, 0x01, remote, 0x0A] 
    s.write(bytearray(command))
    time.sleep(G.sleepCommand)  #give the serial port some time to receive the data

#======================================
# Ask remote to send a data packet of type 0x28 telling us the format of the 
# data packets that will be sent to us when acquisition is started
def getPacketConfig(s, remote):

    command = [0x02, 0x28, 0x01, remote, 0x0A] 
    s.write(bytearray(command))
    time.sleep(G.sleepCommand)  #give the serial port some time to receive the data

#======================================
# Ask remote to send a data packet of type 0x27 telling us the current sensor configuration 
def getFixedConfig(s, remote):

    command = [0x02, 0x27, 0x01, remote, 0x0A] 
    s.write(bytearray(command))
    time.sleep(G.sleepCommand)  #give the serial port some time to receive the data

#======================================
# Ask remote to send a data packet of type 0x29 containing calibration information from sensor. 
def getCalibration(s, sensor, remote):

    command = [0x02, 0x29, 0x02, remote, sensor, 0x0A] 
    s.write(bytearray(command))
    time.sleep(G.sleepCommand)  #give the serial port some time to receive the data

#======================================
# Ask remote to set the current sensor configuration to "config". 
# The response will be an ACK packet if successful, or NACK packet if not. 
def setFixedConfig(s,config,remote):

    command = [0x02, 0x26, 0x02, remote, config, 0x0A] 
    s.write(bytearray(command))
    time.sleep(G.sleepCommand)  #give the serial port some time to receive the data

#======================================
# Start data acquisition. 
# The response will be an ACK packet if successful, or NACK packet if not.
# The remote will asynchronously start sending data packets in the format 
# described by record returned by the "getPacketConfig" command (above). 
# The asynchronous data packets all have the same format and are identified by record type 0x41. 
def startData(s):

    command = [0x02, 0x20, 0x00, 0x0A]
    s.write(bytearray(command))
    time.sleep(G.sleepCommand)  #give the serial port some time to receive the data
    
#======================================
# Stop data acquisition. 
# The response will be an ACK packet if successful, or NACK packet if not.
def stopData(s):

    command = [0x02, 0x21, 0x00, 0x0A]
    s.write(bytearray(command))
    time.sleep(G.sleepCommand)  #give the serial port some time to receive the data

#======================================
# Power down remote. 
# The response will be an ACK packet if successful, or NACK packet if not.
def powerDown(s,remote):

    command = [0x02, 0x2B, 0x01, remote, 0x0A]
    s.write(bytearray(command))
    time.sleep(G.sleepCommand)  #give the serial port some time to receive the data


