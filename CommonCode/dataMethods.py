# system stuff
# system stuff
import time

# local stuff
from pyolabGlobals import G
from commMethods import *
from analClass import A
from iolabInfo import *

"""
These methods are focused on dealing with the data received 
from the IOLab system. The basic idea is that code to fetch 
data from the com port, and code to analyze these data, are 
run from two separate asynchronous threads set up below 
called readDataThread and analyzeDataThread. These in turn
call other methods to manipulate and save the data in useful
ways.

"""

#===============================================
# This starts up the pyolab software framework by:   
#   1) setting up the serial port that the IOLab Dongle is plugged into
#   2) launching asynchronous threads to read data and analyze data 
# 
def startItUp():

    # Start by finding the serial the IOLab port
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
    A.a.analStart()

    # keep looping as long as G.running is True
    while G.running:
        newPointer = analyzeData()
        G.dataPointer = newPointer
        time.sleep(G.sleepTimeAnal)

    print "Exiting analyzeDataThread"

    # user code that is called at the end
    A.a.analEnd()

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
        A.a.analLoop()

        # write data to an output file if the dumpData flag is set
        if G.dumpData:
            #--------replace the part between these lines--------
            dataString = ''
            for i in range(G.dataPointer,dataLength):
                dataString += hex(G.dataList[i])[2:] + ' '
            G.outputFile.write(dataString)
            #--------replace the part between these lines--------

    return dataLength


#======================================
# This method spins through the raw data array and finds the actual data packet records received 
# from the remote. These are described in detail in the USB Interface Specification document 
# (Indesign document number 1814F03 Revision 11, available on the IOLab web page at
#  http://www.iolab.science/Documents/IOLab_Expert_Docs/IOLab_usb_interface_specs.pdf)
#
def findRecords():

    i = G.nextData         # where we will start looking
    iLast = len(G.dataList) # where we will stop looking

    # work through the data looking for valid records and saving these to G.recDict
    # 
    while i < (iLast - 3):
        if (G.dataList[i] == 2):  # find start of packet (SOP) byte = 0x2
            # find record type
            for recType in G.recTypeList:
                if G.dataList[i+1] == recType:

                    # find byte count (BC)
                    # see if we can find the end of packet (EOP) byte = 0xa
                    ndata = G.dataList[i+2]
                    # check that this isn't past the end of the list
                    if i+3+ndata < iLast:
                        if G.dataList[i+3+ndata] == 0xa:
                            # if SOP, BC, and EOP are all consistent then save the record
                            rec = G.dataList[i+2:i+3+ndata]
                            # add record to the appropriate list
                            G.recDict[recType].append(rec)
                            # if the thing we just received was a NACK it means a command was
                            # not properly serviced, so we should tell someone
                            if recType == G.recType_NACK:
                                print " NACK: " + str(rec)

                            # figure out where we are starting next
                            G.nextData = i + 4 + ndata # where the next record starts
                            i = G.nextData - 1         # since we are adding 1 after the break
                            break
                        else:
                            # shouldn't ever get here but check just in case
                            print "guessed wrong recType ' + hex(recType) + ' at i = "+str(i)
                    else:
                        break
            i += 1

        else:
            i += 1


