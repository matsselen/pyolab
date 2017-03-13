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


def DrawList():
        plist = ['Liz','Tom','Chi']

        for item in plist:
                listbox.insert(END,item)

def ok():
    item = var.get()
    listbox.insert(END,item)    
    if show:
    	show = False
    	entry.grid_forget()
    else:
    	show = True
    	entry.grid()


def get(event):
    item = event.widget.get()
    listbox.insert(END,item)    
        
setupGlobalVariables()


#Create & Configure root 
root = Tk()
root.geometry('500x500')
root.title("Root Title")
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)

#Create & Configure frame 
frame=Frame(root)
frame.grid(row=0, column=0, sticky=N+S+E+W)

listbox = Listbox(frame)

show = True
button1 = Button(frame,text = "press me",command = DrawList)
button2 = Button(frame,text = "menu",command = ok)

entry = Entry(frame)
entry.bind('<Return>', get)

var = StringVar(frame)
choices = set(G.cmdTypeNumDict.keys())
var.set(G.cmdTypeNumDict.keys()[0]) # set the default option
popupMenu = OptionMenu(frame, var, *choices)

for row in range(10):
	Grid.rowconfigure(frame, row, weight=1)

Grid.columnconfigure(frame, 0, weight=0)
Grid.columnconfigure(frame, 1, weight=1)
 
listbox.grid(row=0, column=1, rowspan=10, padx=10, pady=10, sticky=W+E+N+S)

button1.grid(row=0, column=0, padx=10, pady=10, sticky=N+E+W)
button2.grid(row=1, column=0, padx=10, pady=10, sticky=N+E+W)
entry.grid(row=2, column=0, padx=10, pady=10, sticky=N+E+W)
popupMenu.grid(row=3, column=0, rowspan=8, padx=10, pady=10, sticky=N+E+W)



root.mainloop()
