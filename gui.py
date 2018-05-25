from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext as tkst

root = Tk()
root.title('Tes')
vertexNum = 1
def log(msg):
    scrolltext.config(state=NORMAL)
    scrolltext.insert(INSERT,msg+'\n')
    scrolltext.config(state=DISABLED)

def drawVertex(event):
    global vertexNum
    x, y = event.x, event.y
    r = 20
    secondcanvas.create_oval(x+r, y+r, x-r,y-r,fill="#00BCD4", outline="#0097A7", width=2, tags=str(vertexNum))
    secondcanvas.create_text(x,y,text=str(vertexNum), tags=str(vertexNum))
    vertexNum +=1
    log('Vertex created at '+str(x)+' and '+str(y))

def delAll(*args):
    secondcanvas.delete("all")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

toolbar = ttk.Frame(mainframe,padding="3 3 12 12")
toolbar.grid(column=0, row=0, sticky=(N, W, E, S))

btnAdd = ttk.Button(toolbar, text="Add")
btnAdd.grid(column=0, row=0, sticky=(N, W, E, S))
#btnAdd.bind("<Button-1>", hello)

btnClear = ttk.Button(toolbar, text="Clear")
btnClear.grid(column=1, row=0, sticky=(N, W, E, S), padx=(10,10))
btnClear.bind("<Button-1>", delAll)

mode = StringVar()
dropdown = ttk.Combobox(toolbar, textvariable=mode, state='readonly')
dropdown['values'] = ("Djikstra", "Prims", "Kruskal", "Coloring", "Fuery")
dropdown.grid(column=2, row = 0, padx=(10,10))
dropdown.current(0)

workspace = ttk.Frame(mainframe,padding="3 3 12 12")
workspace.grid(column=0, row=1, sticky=(N, W, E, S))

scrolltext = tkst.ScrolledText(workspace, width=40, height=10, borderwidth = 5, relief = "sunken",state=DISABLED)
scrolltext.grid(column=1, row = 1, sticky=(N, W, E, S))

secondcanvas = Canvas(workspace, width=720, height=480, borderwidth = 5, relief = "sunken")
secondcanvas.grid(column=0, row = 1, sticky=(N, W, E, S))
secondcanvas.bind("<Button-1>", drawVertex)



root.mainloop()