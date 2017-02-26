# system stuff
import time

# local stuff
from pyolabGlobals import *
from userGlobals import *
from iolabInfo import *

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
    print "analUserLoop() was called " + str(U.userCalls) + " times"

#======================================================================
# User code called whenever new data is detected in the main analysis loop 
#
def analUserLoop():
    U.userCalls += 1


