# system stuff
import os
import sys
import time

# local common code
sys.path.append('../CommonCode/')
from pyolabGlobals import G
from analClass import A
from commMethods import *
from dataMethods import *

# local user code
from userMethods import *

"""
This is example code that opens the serial port,
launches data fetching and data analysis threads, 
and responds to user input

"""

#=========================================
# This is the main code. All it does is open the serial port,
# launch the data fetching and data analysis threads, and then
# go into a loop waiting for user input

# This causes the raw data to be dumped to a file called "data.txt" in
# the working directory
G.dumpData = True

if not startItUp():
    print "Problems getting things started...bye"
    os._exit(1)

# This instantiates an object that holds information about which user analysis
# methods are to be called by the main analysis code. Doing it it this way removes
# the need for the analysis code to know about the user code in advance.
# It is assumed that the methods analUserStart(), analUserEnd(), analUserLoop()
# are all localed in the local file "userMethods.py"
#
anal = A(analUserStart, analUserEnd, analUserLoop)

# Loop to get user commands.
while G.running:
    # take a little nap to allow stuff from the last command to finish
    time.sleep(.2) 

    # ask the user for input
    print "\nEnter command:"
    print "   =n  to set remote configuration to n"
    print "   a   to run acquisition"
    print "   s   to stop acquisition"
    print "   x   to exit\n"

    # wait for user input
    command = raw_input()

    # this block is executed when its time to quit
    if command.count('x') > 0:
        #signal that we want to quit
        shutItDown()

    else:

        if command.count('a') > 0:
            if G.configIsSet:
                print "Calling startData()"
                startData(G.serialPort)
            else:
                print "You need to set a configuration before acquiring data"

        elif command.count('s') > 0:
            print "Calling stopData()"
            stopData(G.serialPort)

        elif command.count('=') > 0:
            n=int(command[1:])
            print "Calling setFixedConfig("+str(n)+")" 
            print configName(n)
            # set the fixed configuration 
            setFixedConfig(G.serialPort,n)

            # ask the system to tell us about its configuration 
            print "Calling getFixedConfig()" 
            getFixedConfig(G.serialPort)

            # ask the system to tell us about its data packet configuration
            print "Calling getPacketConfig()" 
            getPacketConfig(G.serialPort)



