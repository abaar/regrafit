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
        self.lineNum = 1
        self.mode = 'add'
        self.currentvertex = False

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.toolbar = ttk.Frame(self.mainframe,padding="3 3 12 12")
        self.toolbar.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.btnAdd = ttk.Button(self.toolbar, text="Add Mode")
        self.btnAdd.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.btnAdd.bind("<Button-1>", self.addMode)

        self.btnEdit = ttk.Button(self.toolbar, text="Edit Mode")
        self.btnEdit.grid(column=1, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(10,10))
        self.btnEdit.bind("<Button-1>", self.editMode)

        self.btnClear = ttk.Button(self.toolbar, text="Clear All")
        self.btnClear.grid(column=2, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(10,10))
        self.btnClear.bind("<Button-1>", self.delAll)

        self.btnRun = ttk.Button(self.toolbar, text="Run")
        self.btnRun.grid(column=4, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(10,10))
        self.btnRun.bind("<Button-1>", self.run)

        self.dropval = tk.StringVar()
        self.dropdown = ttk.Combobox(self.toolbar, textvariable=self.dropval, state='readonly')
        self.dropdown['values'] = ("Djikstra", "Prims", "Kruskal", "Coloring", "Fuery")
        self.dropdown.grid(column=3, row = 0, padx=(10,10))
        self.dropdown.current(0)

        self.workspace = ttk.Frame(self.mainframe,padding="3 3 12 12")
        self.workspace.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.scrolltext = tkst.ScrolledText(self.workspace, width=40, height=10, borderwidth = 5, relief = "sunken",state=tk.DISABLED)
        self.scrolltext.grid(column=1, row = 1, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.secondcanvas = tk.Canvas(self.workspace, width=720, height=480, borderwidth = 5, relief = "sunken")
        self.secondcanvas.grid(column=0, row = 1, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.secondcanvas.bind("<Button-1>", self.cLeft)
        self.secondcanvas.bind("<Button-2>", self.cRight)
        self.secondcanvas.bind("<Button-3>", self.cRight)
        self.secondcanvas.bind("<B1-Motion>", self.cLeftMotion)
        self.secondcanvas.bind("<B1-ButtonRelease>", self.cLeftRelease)

    def log(self, msg, clear=False):
        msg = str(msg)
        self.scrolltext.config(state=tk.NORMAL)
        if clear == True:
            self.scrolltext.delete('1.0', tk.END)
        else:
            self.scrolltext.insert(tk.INSERT,msg+'\n')
        self.scrolltext.see("end")
        self.scrolltext.config(state=tk.DISABLED)

    def cLeft(self,event):
        x, y = event.x, event.y
        cekmode = self.mode
        self.log(cekmode)
        if cekmode == 'add':
            self.selVertex(x,y)
            self.drawVertex(x,y)
        elif cekmode == 'edit':
            self.selVertex(x,y)
    
    def cLeftMotion(self, event):
        cekmode = self.mode
        x, y = self.secondcanvas.canvasx(event.x), self.secondcanvas.canvasy(event.y)
        if cekmode == 'add':
            vtag = self.currentvertex
            if vtag != False:
                label = self.secondcanvas.find_withtag(vtag)[1]
                self.log(self.secondcanvas.coords(label))
                xline, yline = self.secondcanvas.coords(label)
                if self.secondcanvas.find_withtag('ln'+str(self.lineNum)):
                    self.secondcanvas.coords('ln'+str(self.lineNum),xline,yline, x, y)
                else:
                    self.secondcanvas.create_line((xline,yline, x, y), fill='blue', width=3, tags=('ln'+str(self.lineNum),'lo'+vtag,'line'))
                    
        elif cekmode == 'edit':
            r = 20
            vtag = self.currentvertex
            if  vtag != False:
                v = self.secondcanvas.find_withtag(vtag)
                li = self.secondcanvas.find_withtag('li'+vtag)
                lo = self.secondcanvas.find_withtag('lo'+vtag)
                self.secondcanvas.coords(v[0],x+r, y+r, x-r,y-r)
                self.secondcanvas.coords(v[1],x, y)
                self.log('vtag '+str(v))
                self.log('li '+str(li))
                self.log('lo '+str(lo))
                for i in lo:
                    linecoord = self.secondcanvas.coords(i)
                    self.secondcanvas.coords(i,x,y,linecoord[2],linecoord[3])
                for i in li:
                    linecoord = self.secondcanvas.coords(i)
                    self.secondcanvas.coords(i,linecoord[0],linecoord[1],x,y)
                

    def cLeftRelease(self, event):
        cekmode = self.mode
        if cekmode == 'add':
            vtag = self.isIntersect(event.x,event.y)
            if vtag != False and vtag != self.currentvertex:
                label = self.secondcanvas.find_withtag(vtag)[1]
                self.log(self.secondcanvas.coords(label))
                xver, yver = self.secondcanvas.coords(label)

                if self.secondcanvas.find_withtag('ln'+str(self.lineNum)):
                    linecoord = self.secondcanvas.coords('ln'+str(self.lineNum))
                    self.secondcanvas.coords('ln'+str(self.lineNum),linecoord[0],linecoord[1],xver,yver)
                    self.secondcanvas.addtag_withtag('li'+vtag,'ln'+str(self.lineNum))
                    self.lineNum +=1

        vtag  = self.currentvertex
        if vtag != False:
            v = self.secondcanvas.find_withtag(vtag)
            self.secondcanvas.itemconfigure(v[0],outline = '#0097A7')

    
    def cRight(self, event):
        x, y = event.x, event.y
        self.delVertex(x,y)

    def drawVertex(self, x, y):
        if self.isIntersect(x,y) == False:
            r = 20
            self.secondcanvas.create_oval(x+r, y+r, x-r,y-r,fill="#00BCD4", outline="#0097A7", width=2, tags=('v'+str(self.vertexNum),'circle','vertex'))
            self.secondcanvas.create_text(x,y,text=str(self.vertexNum), tags=('v'+str(self.vertexNum),'label','vertex'))
            self.vertexNum +=1
            self.log('Vertex created at '+str(x)+' and '+str(y))
        else:
            self.log('Can\'t create vertex')
    
    def selVertex(self,x, y):
        vtag =self.isIntersect(x,y)
        self.currentvertex = vtag
        if vtag != False:
            v = self.secondcanvas.find_withtag(vtag)
            self.secondcanvas.itemconfigure(v[0],outline = 'red')

    
    def delVertex(self, x, y):
        vtag = self.isIntersect(x,y)
        if vtag != False:
            self.log('vertex '+str(vtag)+' deleted')
            self.secondcanvas.delete(vtag)
            self.secondcanvas.delete('li'+vtag)
            self.secondcanvas.delete('lo'+vtag)

    
    def isIntersect(self, x, y):
        allver = self.secondcanvas.find_withtag('circle')
        # self.log(str(allver))
        self.log('current pos '+str(x)+' '+str(y))
        for i in allver:
            x1,y1,x2,y2 = self.secondcanvas.coords(i)
            if x>=x1 and y >= y1 and x<=x2 and y<=y2:
                vtag = self.secondcanvas.gettags(i)[0]
                return vtag
            # self.log(str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2))
        return False

    def delAll(self, *args):
        self.secondcanvas.delete("all")
        self.log('',True)

    def getComboVal(self):
        return self.dropval.get()
    
    def run(self, *args):
        comboval = self.getComboVal()
        if comboval == 'Djikstra':
            self.log('Djikstra Run !')
        elif comboval == 'Prims':
            self.log('Prims Run !')
        elif comboval == 'Kruskal':
            self.log('Kruskal Run !')
        elif comboval == 'Coloring':
            self.log('Coloring Run !')
        elif comboval == 'Fuery':
            self.log('Fuery Run !')

    def addMode(self,*args):
        self.mode = 'add'
        self.log(self.mode+' on')

    def editMode(self,*args):
        self.mode = 'edit'
        self.log(self.mode+' on')
