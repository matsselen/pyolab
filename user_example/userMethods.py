# system stuff
import sys
import time

# local common code
sys.path.append('../CommonCode/')
from pyolabGlobals import G

# local user code
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

    nRec = len(G.recDict[G.recType_dataFromRemote])
    if nRec > U.nextRecord:
        for n in range(U.nextRecord,nRec):
            r = G.recDict[G.recType_dataFromRemote][n]
            nSens = r[4] # number of sensors in this data record

            # this should be the same as the number expected for this config
            if nSens != len(G.lastSensorBytes):
                print "sensors found "+str(nSens)+" expected "+str(len(G.lastSensorBytes))

            i = 5        # pointer to info and data from first sensor
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
                    #print "saved "+str(nValidBytes)+" bytes from sensor "+str(thisSensor)
                    nSaved += 1
                else:
                    print "Wrong sensor: " +str(thisSensor)

                i += (2 + G.lastSensorBytes[thisSensor])

        U.nextRecord = nRec




#print '{0}\r'.format(x),




