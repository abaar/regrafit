import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext as tkst
from draggable import Draggable

class Gui(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.vertexNum = 1
        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.toolbar = ttk.Frame(self.mainframe,padding="3 3 12 12")
        self.toolbar.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.btnAdd = ttk.Button(self.toolbar, text="Add")
        self.btnAdd.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        #btnAdd.bind("<Button-1>", hello)

        self.btnClear = ttk.Button(self.toolbar, text="Clear")
        self.btnClear.grid(column=1, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(10,10))
        self.btnClear.bind("<Button-1>", self.delAll)

        self.mode = tk.StringVar()
        self.dropdown = ttk.Combobox(self.toolbar, textvariable=self.mode, state='readonly')
        self.dropdown['values'] = ("Djikstra", "Prims", "Kruskal", "Coloring", "Fuery")
        self.dropdown.grid(column=2, row = 0, padx=(10,10))
        self.dropdown.current(0)

        self.workspace = ttk.Frame(self.mainframe,padding="3 3 12 12")
        self.workspace.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.scrolltext = tkst.ScrolledText(self.workspace, width=40, height=10, borderwidth = 5, relief = "sunken",state=tk.DISABLED)
        self.scrolltext.grid(column=1, row = 1, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.secondcanvas = tk.Canvas(self.workspace, width=720, height=480, borderwidth = 5, relief = "sunken")
        self.secondcanvas.grid(column=0, row = 1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.secondcanvas.bind("<Button-1>", self.drawVertex)

    def log(self, msg):
        self.scrolltext.config(state=tk.NORMAL)
        self.scrolltext.insert(tk.INSERT,msg+'\n')
        self.scrolltext.config(state=tk.DISABLED)

    def drawVertex(self, event):
        x, y = event.x, event.y
        r = 20
        self.secondcanvas.create_oval(x+r, y+r, x-r,y-r,fill="#00BCD4", outline="#0097A7", width=2, tags=str(self.vertexNum))
        self.secondcanvas.create_text(x,y,text=str(self.vertexNum), tags=str(self.vertexNum))
        # circle = Draggable(circle)
        self.vertexNum +=1
        self.log('Vertex created at '+str(x)+' and '+str(y))

    def delAll(self, *args):
        self.secondcanvas.delete("all")