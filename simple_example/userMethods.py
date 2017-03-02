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



