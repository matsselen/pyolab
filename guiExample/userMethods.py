#
# This file is part of PyOLab. https://github.com/matsselen/pyolab
# (C) 2017 Mats Selen <mats.selen@gmail.com>
#
# SPDX-License-Identifier:    BSD-3-Clause
# (https://opensource.org/licenses/BSD-3-Clause)
#

# system stuff
import sys
import time
from Tkinter import *


# local common code
sys.path.append('../PyOLabCode/')
from pyolabGlobals import G
from dataMethods import *
from commMethods import *

# local user code
from userGlobals import U

"""
Files starting with the name "user", like this one, are provided 
so that users can create their own analysis jobs.

These user methods are a handy way to try and isolate the user code from the 
library code.  

In this particular example the user code print out any accelerometer data that 
is received from the remote, and at the end of the job it prints a summary of
the records and data that were received from the system.

"""

#======================================================================
# User code called at the beginning. 
#
def analUserStart():
    print "in analUserStart()"

    U.sensNum = 1
    print "...will dump data from " + sensorName(U.sensNum)

    print "\n MAKE SURE YOUR REMOTE IS TURNED ON \n"

#======================================================================
# User code called at the end. 
#
def analUserEnd():
    print "in analUserEnd()"
    print "analUserLoop() was called " + str(U.analUserCalls) + " times"

    # print information about the records that were received
    for rectype in G.recTypeDict:
        name = G.recTypeDict[rectype]
        count = len(G.recDict[rectype])
        print "found "+str(count) + " records of type " + name
    print " "

    # print information about the sensor data that was received
    for sensor in G.uncalDataDict:
        name = sensorName(sensor)
        count = len(G.uncalDataDict[sensor])
        print "found "+str(count) + " measurements of type " + name
    print " "

#======================================================================
# User code called whenever new data is detected in the main analysis loop 
#
def analUserLoop():
    U.analUserCalls += 1

    # print any new accelerometer data to the screen
    # the sys.stdout.write and .flush makes it appear on the same line
    #
    nData = len(G.allRecList)
    if nData > U.lastRecord:
        for i in range(U.lastRecord,nData):
            recType = G.allRecList[i][0]
            index = G.allRecList[i][1]
            rec = G.recDict[recType][index]

            #U.listBoxCommRx.insert(END,rec)
            #U.listBoxData.insert(END,rec)

            if recType == G.recType_dataFromRemote:
                U.listBoxData.insert(END,rec)
            else:
                U.listBoxCommRx.insert(END,rec)

        U.lastRecord = nData

    
def sendCommand():

    command = G.cmdTypeNumDict[U.selection]    
    pyld = U.payload.split(',')

    if len(pyld) > 0 and U.payload != '':
        payload = [int(pyld[i]) for i in range(len(pyld))]
        nBytes  = len(payload)
        command_record = [0x02, command, nBytes] + payload + [0x0A]

    else:
        command_record = [0x02, command, 0x00, 0x0A]

    U.listBoxCommTx.insert(END,command_record)

    print "calling sendIOLabCommand with record:"
    print command_record
    sendIOLabCommand(G.serialPort,command_record)


def getEntryPrompt(command):

    promptDict = {
        0x14 : ['no payload',''],
        0x20 : ['no payload',''],
        0x21 : ['no payload',''],
        0x22 : ['payload',''],
        0x23 : ['payload: remote','1'],
        0x24 : ['no payload',''],
        0x25 : ['remote','1'],
        0x26 : ['payload: remote, config','1,38'],
        0x27 : ['payload: remote','1'],
        0x28 : ['payload: remote','1'],
        0x29 : ['payload: remote, sensor','1,4'],
        0x2A : ['payload: remote','1'],
        0x2B : ['payload: remote','1']
        }

    print "in getEntryPrompt, command is "+ str(command)
    if command in G.cmdTypeNumDict:
        commandNum = G.cmdTypeNumDict[command]
        prompt = promptDict[commandNum]
        print prompt[0]
        print prompt[1]
    else:
        prompt = 'oops'

    return prompt


