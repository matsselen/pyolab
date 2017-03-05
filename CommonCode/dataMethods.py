# system stuff
import time
import numpy as np

# local stuff
from analClass import AnalysisClass
from pyolabGlobals import G
from commMethods import *
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


#===========================================================================================
# This method spins through the raw data array and finds the actual data packet records received 
# from the remote. These are described in detail in the Indesign USB Interface Specification 
# document that can be found at at Documentation/IOLab_usb_interface_specs.pdf)
# 
# The records are put into dictionary recDict (see pyolabGlobals.py)
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
                            rec = G.dataList[i:i+4+ndata]
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


#=================================================================
# This method looks for changes to the fixed configuration of the 
# IOLab remote (for now just assumes you are using one remote)
#
def findLastConfig():

    # look for fixed config information
    if len(G.recDict[G.recType_getFixedConfig]) > 0:
        fc = G.recDict[G.recType_getFixedConfig][-1][4]   # the latest fixed config
    else:
        fc = 0                                            # or 0 if none found

    # if new, save it and print it
    if fc != G.lastFixedConfig:        
        G.lastFixedConfig = fc
        print "New fixed configuration " + str(fc)


    # look for packet config information
    if len(G.recDict[G.recType_getPacketConfig]) > 0:
        pc = G.recDict[G.recType_getPacketConfig][-1][4:-1] # the latest packet config
    else:
        pc = []                                           # or [] if none found

    # if new, save it and print it
    if pc != G.lastPacketConfig:       
        G.lastPacketConfig = pc

        sc = {}
        for i in range(pc[0]):      # decode the packet config record
            s = pc[i*2+1]           # sensor
            l = pc[i*2+2]           # max data length
            sc[s] = l

        G.lastSensorBytes = sc     # save it
        G.configIsSet = True


        print "New packet configuration " + str(pc)
        print "New sensor configuration " + str(sc)


#===================================================================
# Extracts the payload data from dataFromRemote records and calls 
# extractSensorData() to extract raw sensor data from these 
#
def decodeDataPayloads():
    nRec = len(G.recDict[G.recType_dataFromRemote])
    if nRec > G.nextRecord:
        for n in range(G.nextRecord,nRec):
            r = G.recDict[G.recType_dataFromRemote][n]
            nSens = r[6] # number of sensors in this data record

            # this should be the same as the number expected for this config
            if nSens != len(G.lastSensorBytes):
                print "sensors found "+str(nSens)+" expected "+str(len(G.lastSensorBytes))

            i = 7        # pointer to info and data from first sensor
            nSaved = 0   # the number of sensors we have saved data from
            while nSaved < nSens:
                thisSensor = r[i] & 0x7F            # ID of the current sensor
                sensorOverflow = r[i] > thisSensor  # is overflow bit set?
                recSequence = r[2]                  # byte incremented every record

                # the first couple if records may have the overflow bit set
                if sensorOverflow:
                    print "overflow on recSequence " +str(recSequence)+" sensor "+str(thisSensor)

                # make sure thisSensor is on the list of expected sensors for this config
                if thisSensor in G.lastSensorBytes:
                    nValidBytes = r[i+1]
                    sensorBytes = r[i+2:i+2+nValidBytes]

                    # this is where the the good stuff happens
                    extractSensorData(thisSensor,sensorBytes)
                else:
                    # if we ever get here we need to tell Mats there is a problem. 
                    print "Bailing out after finding wrong sensor: " +str(thisSensor) + " in " + str(r)
                    return

                nSaved += 1

                i += (2 + G.lastSensorBytes[thisSensor])

        G.nextRecord = nRec

#======================================================================
# Extracts the raw (uncalibrated) data from individual sensor sub-payloads. 
# For details see 
#
# Inputs:
#   sensor      the number of the sensor we are decoding as per sensorName()
#   data        the data payload we are decoding
#
# Output:
#   The information is placed in a global dictionary G.uncalDataDict
#   (see pyolabGlobals.py)
#
def extractSensorData(sensor,data):

    # The different code segments below deal with data from different sensors. 
    # Only sensors marked with '*' in the list below are extracted so far
    # (I'm still working on the sensors labeled with '-')
    #
    #  * 'Accelerometer',
    #  * 'Magnetometer',
    #  * 'Gyroscope',
    #  - 'Barometer',
    #  * 'Microphone',
    #  * 'Light',
    #  * 'Force',
    #  * 'Wheel',
    #  - 'ECG3',
    #  - 'Battery',
    #  * 'HighGain',
    #  * 'Analog7',
    #  * 'Analog8',
    #  * 'Analog9',
    #  - 'Thermometer',
    #  - 'ECG9'
    #
    # Note also that the extracted data is uncalibrated. 
    # 


    #-----------------------
    # Accelerometer
    # A 16 bit signed number for each of the three axes.
    # Full scale depends on device settings. Default is 4g. 
    # Calibration needed for both scale and offset. 
    #
    if sensorName(sensor) == 'Accelerometer':
        # data comes in 6 byte blocks
        if(len(data)%6 > 0):
            print "Accelerometer data not a multiple of 6 bytes"
        else:
            nsets = len(data)/6
            for i in range(nsets):
                d = data[i*6:i*6+6]
                d01 = np.int16(d[0]<<8 | d[1])
                d23 = np.int16(d[2]<<8 | d[3])
                d45 = np.int16(d[4]<<8 | d[5])
                # the odd ordering & signs of the data below represent 
                # the fact that the sensor is rotated on the PCB 
                G.uncalDataDict[sensor].append([-d23,d01,d45])

    #-----------------------
    # Magnetometer
    # A 16 bit signed number for each of the three axes.
    # Full scale depends on device settings.
    # Calibration needed for both scale and offset. 
    #
    if sensorName(sensor) == 'Magnetometer':
        # data comes in 6 byte blocks
        if(len(data)%6 > 0):
            print "Magnetometer data not a multiple of 6 bytes"
        else:
            nsets = len(data)/6
            for i in range(nsets):
                d = data[i*6:i*6+6]
                d01 = np.int16(d[0]<<8 | d[1])
                d23 = np.int16(d[2]<<8 | d[3])
                d45 = np.int16(d[4]<<8 | d[5])
                G.uncalDataDict[sensor].append([-d01,-d23,-d45])

    #-----------------------
    # Gyroscope
    # A 16 bit signed number for each of the three axes. Linear with omega.
    # Full scale depends on device settings.
    # Calibration needed for both scale and offset. 
    #
    if sensorName(sensor) == 'Gyroscope':
        # data comes in 6 byte blocks
        if(len(data)%6 > 0):
            print "Gyroscope data not a multiple of 6 bytes"
        else:
            nsets = len(data)/6
            for i in range(nsets):
                d = data[i*6:i*6+6]
                d01 = np.int16(d[0]<<8 | d[1])
                d23 = np.int16(d[2]<<8 | d[3])
                d45 = np.int16(d[4]<<8 | d[5])
                # the odd ordering & signs of the data below represent 
                # the fact that the sensor is rotated on the PCB 
                G.uncalDataDict[sensor].append([-d23,d01,d45])

    #-----------------------
    # Microphone. 
    # Linear with intensity (I assume). Returns 16 bit unsigned number.  
    #
    if sensorName(sensor) == 'Microphone':
        # data comes in 2 byte blocks
        if(len(data)%2 > 0):
            print "Microphone data not a multiple of 2 bytes"
        else:
            nsets = len(data)/2
            for i in range(nsets):
                d = data[i*2:i*2+2]
                d01 = np.uint16(d[0]<<8 | d[1])
                G.uncalDataDict[sensor].append(d01)

    #-----------------------
    # Light
    # Linear with intensity (I assume). Returns 16 bit unsigned number.   
    #
    if sensorName(sensor) == 'Light':
        # data comes in 2 byte blocks
        if(len(data)%2 > 0):
            print "Light data not a multiple of 2 bytes"
        else:
            nsets = len(data)/2
            for i in range(nsets):
                d = data[i*2:i*2+2]
                d01 = np.uint16(d[0]<<8 | d[1])
                G.uncalDataDict[sensor].append(d01)

    #-----------------------
    # Force
    # A 16 bit signed number derived by measuring the B-field of a magnet 
    # that moves in response to an applied force. Linear with force. 
    # Calibration needed for both scale and offset. 
    #
    if sensorName(sensor) == 'Force':
        # data comes in 2 byte blocks
        if(len(data)%2 > 0):
            print "Force data not a multiple of 2 bytes"
        else:
            nsets = len(data)/2
            for i in range(nsets):
                d = data[i*2:i*2+2]
                d01 = np.int16(d[0]<<8 | d[1])
                G.uncalDataDict[sensor].append(d01)

    #-----------------------
    # Wheel
    # A 16 bit signed number. Each measurement is the change of the wheels position 
    # in 1mm increments since the last measurement. Measurement interval is 1/100 sec.  
    #
    if sensorName(sensor) == 'Wheel':
        # data comes in 2 byte blocks
        if(len(data)%2 > 0):
            print "Wheel data not a multiple of 2 bytes"
        else:
            nsets = len(data)/2
            for i in range(nsets):
                d = data[i*2:i*2+2]
                d01 = np.int16(d[0]<<8 | d[1]) # dr
                G.uncalDataDict[sensor].append(d01)

    #-----------------------
    # HighGain
    # G+/G- feeds DC coupled differential op-amp w/ gain 1400
    # Op-amp output feeds internal 12 bit ADC (raw ADC values [0 - 4095])
    # Full scale count is +- 3V/2 = +- 1500 mV
    # Zero offset 0x7FF (half full scale)
    # Full scale deflection = 1500mV/1400 = 1.07 mV
    # counts per volt = 2048 * 1400 / 1500
    # 
    if sensorName(sensor) == 'HighGain':
        # data comes in 2 byte blocks
        if(len(data)%2 > 0):
            print "HighGain data not a multiple of 2 bytes"
        else:
            nsets = len(data)/2
            for i in range(nsets):
                d = data[i*2:i*2+2]
                d01 = np.uint16(d[0]<<8 | d[1])
                G.uncalDataDict[sensor].append(d01)

    #-----------------------
    # Analog7
    # Feeds internal 12 bit ADC (raw ADC values [0 - 4095])
    # Full scale corresponds to either 3.0V or 3.3V depending on configuration
    # (see configName(); if configuration name contains '3V3' reference is 3.3V)
    #
    if sensorName(sensor) == 'Analog7':
        # data comes in 2 byte blocks
        if(len(data)%2 > 0):
            print "Analog7 data not a multiple of 2 bytes"
        else:
            nsets = len(data)/2
            for i in range(nsets):
                d = data[i*2:i*2+2]
                d01 = np.uint16(d[0]<<8 | d[1])
                G.uncalDataDict[sensor].append(d01)

    #-----------------------
    # Analog8
    # Feeds internal 12 bit ADC (raw ADC values [0 - 4095])
    # Full scale corresponds to either 3.0V or 3.3V depending on configuration
    # (see configName(); if configuration name contains '3V3' reference is 3.3V)
    #
    if sensorName(sensor) == 'Analog8':
        # data comes in 2 byte blocks
        if(len(data)%2 > 0):
            print "Analog8 data not a multiple of 2 bytes"
        else:
            nsets = len(data)/2
            for i in range(nsets):
                d = data[i*2:i*2+2]
                d01 = np.uint16(d[0]<<8 | d[1])
                G.uncalDataDict[sensor].append(d01)

    #-----------------------
    # Analog9
    # Feeds internal 12 bit ADC (raw ADC values [0 - 4095])
    # Full scale corresponds to either 3.0V or 3.3V depending on configuration
    # (see configName(); if configuration name contains '3V3' reference is 3.3V)
    #
    if sensorName(sensor) == 'Analog9':
        # data comes in 2 byte blocks
        if(len(data)%2 > 0):
            print "Analog9 data not a multiple of 2 bytes"
        else:
            nsets = len(data)/2
            for i in range(nsets):
                d = data[i*2:i*2+2]
                d01 = np.uint16(d[0]<<8 | d[1])
                G.uncalDataDict[sensor].append(d01)








