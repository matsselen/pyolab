#
# This file is part of PyOLab. https://github.com/matsselen/pyolab
# (C) 2017 Mats Selen <mats.selen@gmail.com>
#
# SPDX-License-Identifier:    BSD-3-Clause
# (https://opensource.org/licenses/BSD-3-Clause)
#

# system stuff
import os
import sys
import time
from Tkinter import *           #This interface allow us to draw windows

# local common code
sys.path.append('../PyOLabCode/')
from analClass import AnalysisClass
from pyolabGlobals import G
from userGlobals import U

from commMethods import *
from setupMethods import *

# local user code
from userMethods import *

def skv(s,k,v):
    kv = ((k&7)<<5) + (v&31)
    return [s,kv]

def dacAction(val):
    fv = float(val)*10
    iv = int(val)
    idvList = skv(25,1,iv)+skv(25,0,1)
    setOutputConfig(G.serialPort,idvList,1)

def b2Action():
    if U.b2['text'] == ' Run ':
        U.b2['text'] = ' Pause '
        if G.configIsSet:
            print "Calling startData()"
            startData(G.serialPort)
            
        else:
            print "You need to set a configuration before acquiring data"
            

    else:
        U.b2['text'] = ' Run '
        print "Calling stopData()"
        stopData(G.serialPort)
        
"""
This is example main() code that creates the GUI, launches data 
fetching and data analysis threads, and responds to user input.

"""

def main():
    

    # ======== START OF GUI SETUP ==============================

    root = Tk()
    root.title('IOLab')
    
    frame1 = Frame(root)
    frame1.pack()
    
    U.dac = Scale(frame1, from_=0, to=31, resolution=1 , label='DAC setting', orient=HORIZONTAL, command=dacAction).pack()

    #U.b1 = Button(frame1, text=' Set ', command=b1Action)
    #U.b1.pack(side=LEFT, fill=NONE)
    
    U.b2 = Button(frame1, text=' Run ', command=b2Action)
    U.b2.pack(side=TOP, fill=NONE)
    
    frame2 = Frame(root)
    frame2.pack()
    
    Label(frame2, text=' ').pack()

    U.txtA7 = StringVar(frame2)
    U.txtA8 = StringVar(frame2)
    U.txtA9 = StringVar(frame2)
    U.txtHG = StringVar(frame2)

    labelA7=Label(frame2, textvariable=U.txtA7, font="TkHeadingFont 16").pack(side=TOP)
    labelA8=Label(frame2, textvariable=U.txtA8, font="TkHeadingFont 16").pack(side=TOP)
    labelA9=Label(frame2, textvariable=U.txtA9, font="TkHeadingFont 16").pack(side=TOP)
    #labelHG=Label(frame2, textvariable=U.txtHG, font="TkHeadingFont 16").pack(side=TOP)



    # ======== END OF GUI SETUP =================

    #============================================================
    # set up IOLab user callback routines
    analClass = AnalysisClass(analUserStart, analUserEnd, analUserLoop)
    
    # start up the IOLab data acquisition stuff
    if not startItUp():
        print "Problems getting things started...bye"
        os._exit(1)

    # setting up analog inputs with 3.3V reference
    setFixedConfig(G.serialPort,12,1)
    print configName(12)
    getFixedConfig(G.serialPort,1)
    getPacketConfig(G.serialPort,1)        
    
    #
    
    #-------------------------------------------
    # this is the main GUI event loop
    root.mainloop()
    
    #-------------------------------------------
    # when we get to this point it means we have quite the GUI
    print "Quitting..."
    
    # shut down the IOLab data acquisition
    shutItDown()

#=====================================================
# run the above main() code 
if __name__ == "__main__":
    main()
