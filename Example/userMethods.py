# system stuff
import sys
import time


# local common code
sys.path.append('../CommonCode/')
from pyolabGlobals import G
from dataMethods import *

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

    for rectype in G.recTypeDict:
        name = G.recTypeDict[rectype]
        count = len(G.recDict[rectype])
        print "found "+str(count) + " records of type " + name
    print " "

    for sensor in G.sensorDataDict:
        name = sensorName(sensor)
        count = len(G.sensorDataDict[sensor])
        print "found "+str(count) + " records of type " + name
    print " "

#======================================================================
# User code called whenever new data is detected in the main analysis loop 
#
def analUserLoop():
    U.analUserCalls += 1

    

