# system stuff
import time
import numpy as np

# local stuff
from analClass import AnalysisClass
from pyolabGlobals import G
from commMethods import *
from dataMethods import *

"""
These methods are focused on setting up the IOLab system, initializing the 
threads to fetch and analyze data, and calling code to analyze these data.

"""

#===============================================
# This starts up the pyolab software framework by:   
#   1) setting up the serial port that the IOLab Dongle is plugged into
#   2) launching asynchronous threads to read data and analyze data 
# 
def startItUp():

    # Start by finding the serial port that the IOLab dongle is plugged into
    portName = getIOLabPortName()
    
    # Open this port if one was found, otherwise quit. 
    if portName != '':

        G.serialPort = openIOLabPort(portName)

        # create and launch a thread that gets data from the serial port
        # this will keep running until the global variable "G.running" is set to False
        G.readThread = Thread(target=readDataThread)
        G.readThread.start()

        # create and launch a thread that analyzes data
        # this will keep running until the global variable "G.running" is set to False
        G.analThread = Thread(target=analyzeDataThread)
        G.analThread.start()

        return True
    else:
        print "Can't open the comm port - is there a dongle plugged in?"
        return False


#===============================================
# This shuts down the pyolab software framework by:   
#   1) signaling the reading and analysis threads to stop
#   2) pausing until these threads have indeed stopped
#   3) sending a signal to the IOLab remote to power itself down 
# 
def shutItDown():

    #signal that we want to quit
    G.running = False
    print "signaling exit"

    #require that each thread finish before exiting
    G.readThread.join()
    G.analThread.join()
    print "all threads finished"

    print "power down remote 1"
    powerDown(G.serialPort)


#=========================================
# This will run in a separate thread to read data from the serial port. 
# It calls readData(), which does the actual work.
#
def readDataThread():

    print "In readDataThread: " + str(G.sleepTimeRead)
  
    # keep looping as long as G.running is True
    while G.running:
        newdata = readData()
        G.dataList.extend(newdata)
        time.sleep(G.sleepTimeRead)

    print "Exiting readDataThread"


#======================================
# Called by readDataThread, which means that this method
# is basically called several times per second to get incoming data from the
# serial port.
#
def readData():

    # This part loads raw serial data into a list. 
    rawList = []
    while G.serialPort.inWaiting() > 0:
        nwait = G.serialPort.inWaiting()
        raw = G.serialPort.read(nwait)
        rawList.append(raw)

        # since the pyserial input buffer seems to be limited to just over 1000 bytes, 
        # send a warning if we are getting too close so we can reduce "sleepTime"
        if nwait > 1000: 
            print str(nwait) + ": careful with that buffer, Eugene"

    # This part takes the raw data and turns in into a list of bytes. 
    dList = []
    while len(rawList) > 0:
        for i in range(0,len(rawList[0])):
            dList.append(ord(rawList[0][i]))   
        del rawList[0]

    # Return the list of bytes
    return dList


#=========================================
# This will run in a separate thread to analyze data
# It calls analyzeData(), which does the actual work.
#
def analyzeDataThread():

    print "In analyzeDataThread: " + str(G.sleepTimeAnal)

    # set up dictionary that will hold data records received on serial port
    for recType in G.recTypeList:
        G.recDict[recType] = []

    if G.dumpData:
        G.outputFile = open('data.txt','w') # file opened in pwd

    # user code that is called at the beginning
    AnalysisClass.handle.analStart()

    # set up the of lists that will hold uncalibrated sensor data
    sensorList = sensorName('SensorList')
    for sensNum in sensorList:
        G.uncalDataDict[sensNum] = []

    # keep looping as long as G.running is True
    while G.running:
        newPointer = analyzeData()
        G.dataPointer = newPointer
        time.sleep(G.sleepTimeAnal)

    print "Exiting analyzeDataThread"

    # user code that is called at the end
    AnalysisClass.handle.analEnd()

    if G.dumpData:
        G.outputFile.close()

#======================================================================
# It is called by analyzeDataThread several times per second on a timer. 
# Each time this method is called there may be new data present in dataList
# since this is filled asynchronously as data packets arrive to the serial port. 
#
def analyzeData():

    # for now just print the data to "outputfile". You should do something 
    # more interesting here (like actually analyzing data for example)

    # dataLength is the length of the dataList "now"
    # G.dataPointer was the value of dataLength the last time this was called,
    # which means that data between these two values is new.
    dataLength = len(G.dataList)
    if dataLength > G.dataPointer:

        # analyze the raw data stream and sort it into records. 
        findRecords()

        # look for a change in configuration
        findLastConfig()

        # extract sensor data information from the data records
        decodeDataPayloads()

        # call user analysis code
        AnalysisClass.handle.analLoop()

        # write data to an output file if the dumpData flag is set
        if G.dumpData:
            dataString = ''
            for i in range(G.dataPointer,dataLength):
                dataString += hex(G.dataList[i])[2:] + ' '
            G.outputFile.write(dataString)

    return dataLength


