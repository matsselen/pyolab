# system stuff
import os
import time

# local stuff
from pyolabGlobals import G
from commMethods import *
from dataMethods import *

"""
Files starting with the name "user", like this one, are provided 
so that users can create their own analysis jobs.
 
This is example code that opens the serial port,
launches data fetching and data analysis threads, 
and responds to user input
"""

#=========================================
# This is the main code. All it does is open the serial port,
# launch the data fetching and data analysis threads, and then
# go into a loop waiting for user input

if not startItUp():
    print "Problems getting things started...bye"
    os._exit(1)

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



