# system stuff
import os
import sys
import time

# local common code
sys.path.append('../CommonCode/')
from commMethods import *

"""
This is example main() code that opens the serial port, asks the 
dongle what its status is, receives the answer, and quits.

"""

#=========================================

def main():

    # Start by finding the serial port that the IOLab dongle is plugged into
    print "\n"
    print "Looking for an IOLab dongle in one of the USB ports..."
    portName = getIOLabPortName()  
    
    # Open this port if one was found, otherwise quit. 
    if portName == '':
        print "Can't open the comm port - is there a dongle plugged in?"
    else:
    
        # open serial port
        G.serialPort = openIOLabPort(portName)
    
        # ask the dongle to send us a status record
        print "Asking the dongle for its status"
        getDongleStatus(G.serialPort)
    
        # Load any waiting raw serial data into a list. 
        rawList = []
        while G.serialPort.inWaiting() > 0:
            nwait = G.serialPort.inWaiting()
            raw = G.serialPort.read(nwait)
            rawList.append(raw)
    
        print "Resulting raw hex data string from serial port:"
        print rawList
    
        print "Powering down the iOLab remote\n"
        powerDown(G.serialPort)
        
#--------------------------
# run the above main() code 
if __name__ == "__main__":
    main()