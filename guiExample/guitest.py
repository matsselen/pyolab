from Tkinter import *           #This interface allow us to draw windows


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
        
root = Tk()                     #This creates a window, but it won't show up
root.geometry('500x500')
root.title("Root Title")

leftframe = Frame(root)
leftframe.pack( side = LEFT , fill=BOTH, expand=1)
Label(leftframe, text="Left Title")

rightframe = Frame(root)
rightframe.pack( side = LEFT , fill=BOTH, expand=1)
Label(rightframe, text="Left Title")

listbox = Listbox(rightframe)
listbox.pack(fill=BOTH, expand=1,padx=10,pady=10)

button = Button(leftframe,text = "press me",command = DrawList)
button.pack(padx=10,pady=10)

button2 = Button(leftframe,text = "menu",command = ok)
button2.pack(padx=10,pady=10)

entry = Entry(leftframe)
entry.pack(side=TOP,padx=10,pady=10)
entry.bind('<Return>', get)

var = StringVar(leftframe)
choices = { 'Pizza','Lasagne','Fries','Fish','Potatoe'}
var.set('Pizza') # set the default option
 
popupMenu = OptionMenu(leftframe, var, *choices)
popupMenu.pack(padx=10,pady=10)


root.mainloop()
