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

def button1Action():
    U.selection = var.get()
    U.payload = entry.get()
    sendCommand()


def commandSelect(event):
    select = var.get()
    print select
    U.selection = select
    prompt = getEntryPrompt(select)
    entry.delete(0, END)
    entry.insert(0,prompt)
 
#============================================================
# set up IOLab user callback routines
analClass = AnalysisClass(analUserStart, analUserEnd, analUserLoop)

# start up the IOLab data acquisition stuff
if not startItUp():
    print "Problems getting things started...bye"
    os._exit(1)

#============================================================
# Create and format the graphical elements that this example uses.  
# This takes many inches of code because Tkinter is not that fancy 
# (and also, I suspect, because I'm not that smart)

# create the root window
root = Tk()
root.geometry('800x600')
root.title("IOLab Test Application")

#-------------------------------------------
# the left part of the screen holds control elements
# this frame does not expand when the window is scaled
leftframe = Frame(root)
leftframe.pack( side = LEFT , fill=BOTH, expand=0)

# mats crappy way of adding some whitespace at the top
Label(leftframe, text="\n\n\n").pack() 

# the drop-down menu will contain a list of possible commands
# and these need to be put into a StringVar object
var = StringVar(leftframe)
commandNames = set(G.cmdTypeNumDict.keys()) # list of possible commands
defaultCommandString = G.cmdTypeNumDict.keys()[0]
var.set(defaultCommandString)  # set the default command

# set up the drop-down menu using the above list of commands
Label(leftframe, text="Select command and \nprovide required playload").pack()
commMenu = OptionMenu(leftframe, var, *commandNames, command = commandSelect)
commMenu.pack(side=TOP, fill=X,padx=10,pady=10)

# the entry box is for commands that require user data
entry = Entry(leftframe)
entry.pack(side=TOP,padx=10,pady=10)
entry.insert(0,getEntryPrompt(defaultCommandString))

# the button is for sending selected commands to IOLab
button1 = Button(leftframe,text = "Send Command",command = button1Action)
button1.pack(side=TOP, padx=10,pady=10)

#-------------------------------------------
# the right part of the screen displays data and control records
# this frame DOES expand when the window is scaled
rightframe = Frame(root)
rightframe.pack( side = LEFT, fill=BOTH, expand=1)
Label(rightframe, text="Control Records Sent / Control Records Received / Data Records Received").pack() 

# scrollable text-box to display COMMAND records
# create a child frame to hold Tx and Rx listboxes
cframe = Frame(rightframe)
cframe.pack(side = TOP , fill=BOTH, expand=0)

# create a child frame to hold the listbox and scrollbar
cTxframe = Frame(cframe)
cTxframe.pack(side = TOP , fill=BOTH, expand=1)

# create scrollbar and Tx listbox and bind them together
scrollbarCommTx = Scrollbar(cTxframe, orient=VERTICAL)
U.listBoxCommTx = Listbox(cTxframe, yscrollcommand=scrollbarCommTx.set)
scrollbarCommTx.config(command=U.listBoxCommTx.yview)
scrollbarCommTx.pack(side=RIGHT, fill=Y)
U.listBoxCommTx.pack(fill=BOTH, expand=1,padx=5,pady=5)

# create a child frame to hold the Rx listbox and scrollbar
cRxframe = Frame(cframe)
cRxframe.pack(side = TOP , fill=BOTH, expand=1)

# create scrollbar and Rx listbox and bind them together
scrollbarCommRx = Scrollbar(cRxframe, orient=VERTICAL)
U.listBoxCommRx = Listbox(cRxframe, yscrollcommand=scrollbarCommRx.set)
scrollbarCommRx.config(command=U.listBoxCommRx.yview)
scrollbarCommRx.pack(side=RIGHT, fill=Y)
U.listBoxCommRx.pack(fill=BOTH, expand=1,padx=5,pady=5)

# scrollable text-box to display DATA records
# create a child frame to hold the listbox and scrollbar
dframe = Frame(rightframe)
dframe.pack(side = TOP , fill=BOTH, expand=1)

# create scrollbar and data listbox and bind them together
scrollbarData = Scrollbar(dframe, orient=VERTICAL)
U.listBoxData = Listbox(dframe, yscrollcommand=scrollbarData.set)
scrollbarData.config(command=U.listBoxData.yview)
scrollbarData.pack(side=RIGHT, fill=Y)
U.listBoxData.pack(fill=BOTH, expand=1,padx=5,pady=5)

#-------------------------------------------
# this is the main GUI event loop
root.mainloop()

#-------------------------------------------
# when we get to this point it means we have quite the GUI
print "Quitting..."

# shut down the IOLab data acquisition
shutItDown()
