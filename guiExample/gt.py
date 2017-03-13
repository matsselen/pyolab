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
    #root.quit()

def get(event):
    item = event.widget.get()
    listbox.insert(END,item)    
        
setupGlobalVariables()

root = Tk()
root.geometry('500x500')
root.title("Root Title")


listbox = Listbox(root)

button1 = Button(root,text = "press me",command = DrawList)
button2 = Button(root,text = "menu",command = ok)

entry = Entry(root)
entry.bind('<Return>', get)

var = StringVar(root)
choices = set(G.cmdTypeNumDict.keys())
var.set(G.cmdTypeNumDict.keys()[0]) # set the default option
popupMenu = OptionMenu(root, var, *choices)

listbox.grid(row=0, column=1)
button1.grid(row=0, column=0, padx=10, pady=10)
button2.grid(row=1, column=0, padx=10, pady=10)
entry.grid(row=2, column=0, padx=10, pady=10)
popupMenu.grid(row=3, column=0, padx=10, pady=10)



root.mainloop()
