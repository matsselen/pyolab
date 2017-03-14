# system stuff
import os
import sys
import time
from Tkinter import *           #This interface allow us to draw windows

# local common code
sys.path.append('../PyOLabCode/')
from analClass import AnalysisClass
from pyolabGlobals import G
from commMethods import *
from setupMethods import *

# local user code
from userMethods import *

def button1Action():
    item1 = var.get()
    item2 = entry.get()
    G.listBoxData.insert(END,[item1,item2]) 
    G.listBoxComm.insert(END,[item1,item2])    
    #root.quit()

def get(event):
    item = event.get()
    G.listBoxData.insert(END,item) 
    G.listBoxComm.insert(END,item)   

def commandSelect(event):
    item2 = entry.get()
    G.listBoxComm.insert(END,[event,item2])    


#============================================================
# set up IOLab user callback routines
analClass = AnalysisClass(analUserStart, analUserEnd, analUserLoop)

# start up the IOLab data acquisition stuff
if not startItUp():
    print "Problems getting things started...bye"
    os._exit(1)

#============================================================
# Create the windows and buttons we will need in this example. 
# This takes many inches of code because Tkinter is not that fancy 
# (and also, I suspect, because I'm not that smart)

# create the root window
root = Tk()
root.geometry('800x500')
root.title("IOLab Test Application")

#-------------------------------------------
# the left part of the screen holds control elements
# this frame does not expand when the window is scaled
leftframe = Frame(root)
leftframe.pack( side = LEFT , fill=BOTH, expand=0)
Label(leftframe, text="Controls").pack()

# the button is for sending selected commands to IOLab
button1 = Button(leftframe,text = "Send Command",command = button1Action)
button1.pack(side=TOP, padx=10,pady=10)

# the entry box is for commands that require user data
entry = Entry(leftframe)
entry.bind('<Return>', get) # look for user hitting <CR>
entry.pack(side=TOP,padx=10,pady=10)

# the drop-down menu will contain a list of possible commands
# and these need to be put into a StringVar object
var = StringVar(leftframe)
commandNames = set(G.cmdTypeNumDict.keys()) # list of possible commands
var.set(G.cmdTypeNumDict.keys()[0])         # set the default command

# set up the drop-down menu using the above list of commands
commMenu = OptionMenu(leftframe, var, *commandNames, command = commandSelect)
commMenu.pack(side=TOP, fill=X,padx=10,pady=10)

#-------------------------------------------
# the right part of the screen displays data and control records
# this frame does expand when the window is scaled
rightframe = Frame(root)
rightframe.pack( side = LEFT , fill=BOTH, expand=1)

# labeled scrollable text-box to display COMMAND records
# put the label in the parent frame
Label(rightframe, text="Control Records").pack() 

# create a child frame to hold the listbox and scrollbar
cframe = Frame(rightframe)
cframe.pack(side = TOP , fill=BOTH, expand=1)

# create scrollbar and listbox and bind them together
scrollbarComm = Scrollbar(cframe, orient=VERTICAL)
G.listBoxComm = Listbox(cframe, yscrollcommand=scrollbarComm.set)
scrollbarComm.config(command=G.listBoxComm.yview)
scrollbarComm.pack(side=RIGHT, fill=Y)
G.listBoxComm.pack(fill=BOTH, expand=1,padx=10,pady=10)

# labeled scrollable text-box to display DATA records
# put the label in the parent frame
Label(rightframe, text="Data Records").pack()

# create a child frame to hold the listbox and scrollbar
dframe = Frame(rightframe)
dframe.pack(side = TOP , fill=BOTH, expand=1)

# create scrollbar and listbox and bind them together
scrollbarData = Scrollbar(dframe, orient=VERTICAL)
G.listBoxData = Listbox(dframe, yscrollcommand=scrollbarData.set)
scrollbarData.config(command=G.listBoxData.yview)
scrollbarData.pack(side=RIGHT, fill=Y)
G.listBoxData.pack(fill=BOTH, expand=1,padx=10,pady=10)

#-------------------------------------------
# this is the main GUI event loop
root.mainloop()

#-------------------------------------------
# when we get to this point it means we have quite the GUI
print "Quitting..."

# shut down the IOLab data acquisition
shutItDown()
