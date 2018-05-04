from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext as tkst

root = Tk()
root.title('Tes')

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

scrolltext = tkst.ScrolledText(mainframe, width=40, height=10, borderwidth = 5, relief = "sunken")
scrolltext.grid(column=1, row = 1, sticky=(N, W, E, S))


def hello(*args):
    txt = scrolltext.get(1.0, END)
    scrolltext.insert(INSERT,txt+'Haha')

secondcanvas = Canvas(mainframe, width=40, height=10, borderwidth = 5, relief = "sunken")
secondcanvas.grid(column=0, row = 1, sticky=(N, W, E, S))
secondcanvas.bind("<Button-1>", hello)



root.mainloop()