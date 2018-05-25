from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext as tkst

root = Tk()
root.title('Tes')

def hello(*args):
    # txt = scrolltext.get(1.0, END)
    scrolltext.insert(INSERT,'Haha\n')

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

toolbar = ttk.Frame(mainframe,padding="3 3 12 12")
toolbar.grid(column=0, row=0, sticky=(N, W, E, S))

btnAdd = ttk.Button(toolbar, text="Add")
btnAdd.grid(column=0, row=0, sticky=(N, W, E, S))
btnAdd.bind("<Button-1>", hello)

mode = StringVar()
dropdown = ttk.Combobox(toolbar, textvariable=mode, state='readonly')
dropdown['values'] = ("Djikstra", "Prims", "Kruskal", "Coloring", "Fuery")
dropdown.grid(column=1, row = 0)
dropdown.current(0)

workspace = ttk.Frame(mainframe,padding="3 3 12 12")
workspace.grid(column=0, row=1, sticky=(N, W, E, S))

scrolltext = tkst.ScrolledText(workspace, width=40, height=10, borderwidth = 5, relief = "sunken")
scrolltext.grid(column=1, row = 1, sticky=(N, W, E, S))

secondcanvas = Canvas(workspace, width=720, height=480, borderwidth = 5, relief = "sunken")
secondcanvas.grid(column=0, row = 1, sticky=(N, W, E, S))
secondcanvas.bind("<Button-1>", hello)



root.mainloop()