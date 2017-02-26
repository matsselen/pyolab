# system stuff
import os
import sys

# local stuff
from pyolabGlobals import *
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
    print "\nEnter command:"
    print "   a   to run acquisition"
    print "   s   to stop acquisition"
    print "   p   to get remote data packet structure"
    print "   c   to get remote sensor configuration"
    print "  =nn  to set remote configuration to nn"
    print "   x   to exit"

    command = raw_input()

    # this block is executed when its time to quit
    if command.count('x') > 0:
        #signal that we want to quit
        shutItDown()

    else:

        if command.count('a') > 0:
            print "startData"
            startData(G.serialPort)

        elif command.count('s') > 0:
            print "stopData"
            stopData(G.serialPort)

        elif command.count('p') > 0:
            print "getPacketConfig"
            getPacketConfig(G.serialPort)

        elif command.count('c') > 0:
            print "getFixedConfig"
            getFixedConfig(G.serialPort)

        elif command.count('=') > 0:
            n=int(command[1:])
            print "setFixedConfig " +str(n)
            print configName(n)
            setFixedConfig(G.serialPort,n)
