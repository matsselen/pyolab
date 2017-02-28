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

    sensor = 1 #accelerometer
    # use the latest packet configuration and find where the sensor data is
    findLastPacketConfig(sensor)





#======================================
#
def findLastPacketConfig(s):

    if len(G.recDict[G.recType_getPacketConfig]) > 0:
        pc = G.recDict[G.recType_getPacketConfig][-1][2:] # the latest packet config
    else:
        pc = []                                             # or [] if none found

    if pc != U.lastPacketConfig:
        print "New packet configuration " + str(pc)
        U.lastPacketConfig = pc
        G.configIsSet = True


#print '{0}\r'.format(x),

