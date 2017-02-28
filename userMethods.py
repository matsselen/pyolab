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
    findLastPacketConfig()

    # if we know the packet configuration...
    #if U.lastPacketConfig != []:
        # then lets see if our sensor is in there


#print '{0}\r'.format(x),

#======================================
#
def findLastPacketConfig():

    if len(G.recDict[G.recType_getPacketConfig]) > 0:
        pc = G.recDict[G.recType_getPacketConfig][-1][2:] # the latest packet config
    else:
        pc = []                                             # or [] if none found

    sc = []
    if pc != U.lastPacketConfig:
        
        U.lastPacketConfig = pc
        G.configIsSet = True
        for i in range(pc[0]):
            sc.append(pc[i*2+1:i*2+3])
            
        print "New packet configuration " + str(pc)
        print "New sensor configuration " + str(sc)



