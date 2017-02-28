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
    findLastPacketConfig()


#======================================================================
# User code called whenever new data is detected in the main analysis loop 
#
def analUserLoop():
    U.analUserCalls += 1

    # keep looking 


#======================================
#
def findLastPacketConfig():

    if G.recType_getPacketConfig in G.recDict:
        print G.recDict[G.recType_getPacketConfig]
    else:
        print "no packet info found"
