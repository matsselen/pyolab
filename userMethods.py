# system stuff
import time

# local stuff
from pyolabGlobals import G
from userGlobals import U

"""
Files starting with the name "user", like this one, are provided 
so that users can create their own analysis jobs.

These user methods are a handy way to try and isolate the user code from the 
library code.  

"""

#======================================================================
# User code called at the beginning. 
#
def analUserStart():
    print "in analUserStart()"

#======================================================================
# User code called at the end. 
#
def analUserEnd():
    print "in analUserEnd()"
    print "analUserLoop() was called " + str(U.analUserCalls) + " times"


#======================================================================
# User code called whenever new data is detected in the main analysis loop 
#
def analUserLoop():
    U.analUserCalls += 1

    # use the latest packet configuration and find where the sensor data is
    findLastConfig()

    nRec = len(G.recDict[G.recType_dataFromRemote])
    if nRec > U.nextRecord:
        for n in range(U.nextRecord,nRec):
            r = G.recDict[G.recType_dataFromRemote][n]
            nSens = r[4] # number of sensors in this data record

            # this should be the same as the number expected for this config
            if nSens != len(U.lastSensorBytes):
                print "sensors found "+str(nSens)+" expected "+str(len(U.lastSensorBytes))

            i = 5        # pointer to info and data from first sensor
            nSaved = 0   # the number of sensors we have saved data from
            #
            while nSaved < nSens:
                thisSensor = r[i] & 0x7F            # ID of the current sensor
                sensorOverflow = r[i] > thisSensor  # is overflow bit set?
                recSequence = r[2]                  # byte incremented every record

                # the first couple if records may have the overflow bit set
                if sensorOverflow:
                    print "overflow on recSequence " +str(recSequence)+" sensor "+str(thisSensor)

                # make sure thisSensor is on the list of expected sensors for this config
                if thisSensor in U.lastSensorBytes:
                    nValidBytes = r[i+1]
                    sensorBytes = r[i+2:i+2+nValidBytes]
                    #print "saved "+str(nValidBytes)+" bytes from sensor "+str(thisSensor)
                    nSaved += 1
                else:
                    print "Wrong sensor: " +str(thisSensor)

                i += (2 + U.lastSensorBytes[thisSensor])

        U.nextRecord = nRec




#print '{0}\r'.format(x),

#======================================
#
def findLastConfig():

    # look for fixed config information
    if len(G.recDict[G.recType_getFixedConfig]) > 0:
        fc = G.recDict[G.recType_getFixedConfig][-1][2]   # the latest fixed config
    else:
        fc = 0                                            # or 0 if none found

    # if new, save it and print it
    if fc != U.lastFixedConfig:        
        U.lastFixedConfig = fc
        print "New fixed configuration " + str(fc)


    # look for packet config information
    if len(G.recDict[G.recType_getPacketConfig]) > 0:
        pc = G.recDict[G.recType_getPacketConfig][-1][2:] # the latest packet config
    else:
        pc = []                                           # or [] if none found

    # if new, save it and print it
    if pc != U.lastPacketConfig:       
        U.lastPacketConfig = pc

        sc = {}
        for i in range(pc[0]):      # decode the packet config record
            s = pc[i*2+1]           # sensor
            l = pc[i*2+2]           # max data length
            sc[s] = l

        U.lastSensorBytes = sc     # save it
        G.configIsSet = True


        print "New packet configuration " + str(pc)
        print "New sensor configuration " + str(sc)





