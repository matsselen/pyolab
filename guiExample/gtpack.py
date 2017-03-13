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

leftframe = Frame(root)
leftframe.pack( side = LEFT , fill=BOTH, expand=1)
l=Label(leftframe, text="Left Title")
l.pack()

rightframe = Frame(root)
rightframe.pack( side = LEFT , fill=BOTH, expand=1)
l=Label(rightframe, text="Left Title")
l.pack()

listbox = Listbox(rightframe)

button = Button(leftframe,text = "press me",command = DrawList)

button2 = Button(leftframe,text = "menu",command = ok)

entry = Entry(leftframe)
entry.bind('<Return>', get)

var = StringVar(leftframe)
choices = set(G.cmdTypeNumDict.keys())
var.set(G.cmdTypeNumDict.keys()[0]) # set the default option
popupMenu = OptionMenu(leftframe, var, *choices)


listbox.pack(fill=BOTH, expand=1,padx=10,pady=10)
button.pack(padx=10,pady=10)
button2.pack(padx=10,pady=10)
entry.pack(side=TOP,padx=10,pady=10)
popupMenu.pack(side=TOP, fill=X,padx=10,pady=10)


root.mainloop()
