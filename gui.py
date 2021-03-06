import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext as tkst
import math
import webbrowser

from line import Line
from vertex import Vertex
from myobject import MyObject
import random

class Gui(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def popWindow(self,labeltext="Isi berat/jarak (integer):",popvalue = 1,nextmode='run'):
        top=self.top=tk.Toplevel(self, padx=30 , pady=10, width=2000)
        self.mode = 'popWindow'
        self.popvalue = popvalue # default value aja
        self.top.resizable(0,0)
        self.poplabel=ttk.Label(top,text=labeltext)
        self.poplabel.pack()
        self.popentry=ttk.Entry(top)
        self.popentry.insert(tk.END,str(popvalue))
        self.popentry.pack()
        self.popbutton=ttk.Button(top,text="Ok",command=lambda:self.cleansubmit(labeltext,nextmode))
        self.popbutton.pack()
        top.protocol("WM_DELETE_WINDOW", lambda:self.onClosing(top,nextmode))
    
    def onClosing(self,top,nextmode):
        top.destroy()
        self.mode = nextmode

    def cleansubmit(self,text,nextmode):
        try:
            value=int(self.popentry.get())
            if value > 0:
                self.top.destroy()
                self.popvalue=value
                self.mode = nextmode
            else:
                self.onPopError(labeltext=text,nextmode=nextmode,popvalue=self.popvalue)

        except ValueError:
            self.onPopError(labeltext=text,nextmode=nextmode,popvalue=self.popvalue)

    def onPopError(self,labeltext="Isi berat/jarak (integer):",popvalue = 1,nextmode = 'run'):
        self.top.destroy()
        messagebox.showwarning("Error Occured", "Masukkan bilangan bulat positif lebih dari 0, jangan yang lain!")
        self.popWindow(labeltext=labeltext,popvalue=popvalue,nextmode=nextmode)
        self.wait_window(self.top)

    # untuk buat tampilan-tampilannnya
    def create_widgets(self):
        self.vertexNum = 1
        self.lineNum = 1
        self.mode = 'add'
        self.currentvertex = False
        self.myobject = MyObject()
        self.lines=[]
        self.vertice=[]
        self.popvalue=-1
        self.animatedprim=[]
        self.linecolor='green'
        self.linesaver=[]
        self.idx=0


        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.toolbar = ttk.Frame(self.mainframe,padding="3 3 12 12")
        self.toolbar.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        self.btnAdd = ttk.Button(self.toolbar, text="Add Mode",state='disabled')
        self.btnAdd.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.btnAdd.bind("<Button-1>", self.addMode)

        self.btnEdit = ttk.Button(self.toolbar, text="Edit Mode")
        self.btnEdit.grid(column=1, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(10,10))
        self.btnEdit.bind("<Button-1>", self.editMode)

        self.btnClear = ttk.Button(self.toolbar, text="Clear All")
        self.btnClear.grid(column=2, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(10,10))
        self.btnClear.bind("<Button-1>", self.delAll)

        self.btnRun = ttk.Button(self.toolbar, text="Run")
        self.btnRun.grid(column=5, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(10,10))
        self.btnRun.bind("<Button-1>", self.run)

        self.btnStop = ttk.Button(self.toolbar, text="Stop",state='disabled')
        self.btnStop.grid(column=6, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(10,10))
        self.btnStop.bind("<Button-1>", self.stop)

        self.btnAbout = ttk.Button(self.toolbar, text="About")
        self.btnAbout.grid(column=7, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(10,10))
        self.btnAbout.bind("<Button-1>", self.about)

        self.btnRandom = ttk.Button(self.toolbar, text="Random Vertex")
        self.btnRandom.grid(column=3, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=(10,10))
        self.btnRandom.bind("<Button-1>", self.randomVertex)

        self.dropval = tk.StringVar()
        self.dropdown = ttk.Combobox(self.toolbar, textvariable=self.dropval, state='readonly')
        self.dropdown['values'] = ("Djikstra", "Prims", "Kruskal", "Naive Coloring","N Max Coloring" ,"Fuery")
        self.dropdown.grid(column=4, row = 0, padx=(10,10))
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
        self.secondcanvas.bind("<Double-Button-1>", self.cLeftDouble)


    #Fungsi untuk menampilkan log di scrolltext
    def log(self, msg, clear=False):
        msg = str(msg)
        self.scrolltext.config(state=tk.NORMAL)
        if clear == True:
            self.scrolltext.delete('1.0', tk.END)
        else:
            self.scrolltext.insert(tk.INSERT,msg+'\n')
        self.scrolltext.see("end")
        self.scrolltext.config(state=tk.DISABLED)

    # Fungsi yang dijalankan ketika user klik kiri mouse
    def cLeft(self,event):
        x, y = event.x, event.y
        cekmode = self.mode
        # self.log(cekmode)
        if cekmode == 'add':
            self.selVertex(x,y)
            self.drawVertex(x,y)
        elif cekmode == 'edit':
            self.selVertex(x,y)

    # Fungsi yang dijalankan ketika user menggerakkan klik kiri mouse
    def cLeftMotion(self, event):
        cekmode = self.mode
        x, y = self.secondcanvas.canvasx(event.x), self.secondcanvas.canvasy(event.y)
        if cekmode == 'add':
            vtag = self.currentvertex
            if vtag != False:
                label = self.secondcanvas.find_withtag(vtag)[1]
                xline, yline = self.secondcanvas.coords(label)
                # jika udah dibuat linenya tinggal di configure coor nya
                if self.secondcanvas.find_withtag('ln'+str(self.lineNum)):
                    self.secondcanvas.coords('ln'+str(self.lineNum),xline,yline, x, y)
                # klo belum di buat linenya ya dibuat
                else:
                    line = self.secondcanvas.create_line((xline,yline, x, y), fill='blue', width=3, tags=('ln'+str(self.lineNum),'lo'+vtag,'line'))
                    # line ditaruh paling bawah
                    self.secondcanvas.tag_lower(line)
                    
        elif cekmode == 'edit':
            r = 20
            vtag = self.currentvertex
            if  vtag != False:
                v = self.secondcanvas.find_withtag(vtag)
                li = self.secondcanvas.find_withtag('li'+vtag)
                lo = self.secondcanvas.find_withtag('lo'+vtag)
                
                self.secondcanvas.coords(v[0],x+r, y+r, x-r,y-r)
                self.secondcanvas.coords(v[1],x, y)
                for i in lo:
                    linecoord = self.secondcanvas.coords(i)
                    self.secondcanvas.coords(i,x,y,linecoord[2],linecoord[3])
                    #configure line label
                    xLineLabel = (x+linecoord[2])/2
                    yLineLabel = (y+linecoord[3])/2
                    # i + 1 karena pasti habis line ada label linenya
                    self.secondcanvas.coords(i+1,xLineLabel,yLineLabel)
                for i in li:
                    linecoord = self.secondcanvas.coords(i)
                    self.secondcanvas.coords(i,linecoord[0],linecoord[1],x,y)
                    #configure line label                    
                    xLineLabel = (x+linecoord[0])/2
                    yLineLabel = (y+linecoord[1])/2
                    self.secondcanvas.coords(i+1,xLineLabel,yLineLabel)


    # Fungsi yang dijalankan ketika user melepas klik kiri mouse
    def cLeftRelease(self, event):
        cekmode = self.mode
        curvtex = self.currentvertex # isinya tag vertex awal
        if cekmode == 'add':
            vtag = self.isIntersect(event.x,event.y) #isinya tag vertex tujuan
            #cek line yg sudah terbuat dari cLeftMotion masih adakah ?
            cekline = self.secondcanvas.find_withtag('ln'+str(self.lineNum)) 
           
           #jika vertex tujuan != false dan vertex tujuan !=vertex awal dan line hasil cLM sudah terbuat
            if vtag != False and curvtex!=False and vtag != curvtex and cekline:
                #simpan coor vertex tujuan
                label = self.secondcanvas.find_withtag(vtag)[1]
                # self.log(self.secondcanvas.coords(label))
                xver, yver = self.secondcanvas.coords(label)

                #configure line agar line endpoint = coor vertex tujuan
                linecoord = self.secondcanvas.coords('ln'+str(self.lineNum))
                self.secondcanvas.coords('ln'+str(self.lineNum),linecoord[0],linecoord[1],xver,yver)
                self.secondcanvas.addtag_withtag('li'+vtag,'ln'+str(self.lineNum))

                #cek apakah sudah ada line yg terbentuk sebelumnya
                counter = 0
                for i in self.secondcanvas.find_withtag('line'):
                    linetag = self.secondcanvas.gettags(i)
                    if ('li'+curvtex in linetag or 'lo'+curvtex in linetag) and ('li'+vtag in linetag or 'lo'+vtag in linetag):
                        counter+=1
                        if counter>1:
                            self.secondcanvas.delete('ln'+str(self.lineNum))
                            self.log('Gagal, kedua vertex sudah terhubung')

                #jika line hasil cLeftMotion saja yg terdeteksi
                if counter==1:
                    # self.log('Berhasil membuat Line')
                    # self.log('di '+str(linecoord))
                    self.popWindow(nextmode='add')
                    self.wait_window(self.top)
                    self.secondcanvas.addtag_withtag(str(self.popvalue),'ln'+str(self.lineNum)) #beratnya = popvalue
                    
                    #Add label for berat here
                    xLineLabel = (linecoord[0]+linecoord[2])/2
                    yLineLabel = (linecoord[1]+linecoord[3])/2
                    self.secondcanvas.create_text(xLineLabel,yLineLabel,text=str(self.popvalue), font=(200), tags=('lb'+str(self.lineNum),'label','lbo'+str(curvtex),'lbi'+str(vtag)))
                    self.lineNum +=1

                # self.log('Jumlah line : '+str(self.lineNum-1))

            # selain if diatas => gagal dan delete line yg dibuat
            else:
                self.secondcanvas.delete('ln'+str(self.lineNum))
                # self.log('Gagal membuat line')

        # untuk mengembalikan warna outline vertex setelah di select
        if curvtex != False:
            v = self.secondcanvas.find_withtag(curvtex)
            self.secondcanvas.itemconfigure(v[0],outline = '#0097A7')

    def cLeftDouble(self,event):
        x, y = event.x, event.y
        isLine = self.isIntersect(x,y,'line')
        if isLine:
            lineId = self.secondcanvas.find_withtag(isLine)
            lineTag = self.secondcanvas.gettags(isLine)
            lineWeight = lineTag[4]
            self.secondcanvas.dtag(lineId,lineWeight)
            self.popWindow(popvalue=lineWeight,nextmode='edit')
            self.wait_window(self.top)
            self.secondcanvas.addtag_withtag(self.popvalue,lineId)
            lineTag = self.secondcanvas.gettags(isLine)
            # self.log('after lagi lagi :'+str(lineTag))
            self.secondcanvas.itemconfigure(lineId[0]+1,text=str(self.popvalue))
            self.log("Bobot vertex "+lineTag[1][3:]+" ke "+lineTag[3][3:]+" menjadi "+str(self.popvalue))

            


    # Fungsi yang dijalankan ketika user klik kanan mouse
    def cRight(self, event):
        x, y = event.x, event.y
        isLine = self.isIntersect(x,y,'line')
        if isLine:
            self.delLine(x,y,isLine)
        else:    
            self.delVertex(x,y)

    # Fungsi untuk draw vertex
    def drawVertex(self, x, y):
        if self.isIntersect(x,y) == False:
            r = 20
            self.secondcanvas.create_oval(x+r, y+r, x-r,y-r,fill="#00BCD4", outline="#0097A7", width=2, tags=('v'+str(self.vertexNum),'circle','vertex'))
            self.secondcanvas.create_text(x,y,text=str(self.vertexNum), font=(200), tags=('v'+str(self.vertexNum),'label','vertex'))
            self.vertexNum +=1
            # self.log('Vertex created at '+str(x)+' and '+str(y))
        # else:
            # self.log('Can\'t create vertex')
    
    # Fungsi untuk select vertex
    def selVertex(self,x, y):
        vtag =self.isIntersect(x,y)
        self.currentvertex = vtag
        if vtag != False:
            v = self.secondcanvas.find_withtag(vtag)
            self.secondcanvas.itemconfigure(v[0],outline = 'red')
    
    # Fungsi untuk delete vertex
    def delVertex(self, x, y):
        vtag = self.isIntersect(x,y)
        if vtag != False:
            self.log('Vertex '+str(vtag)+' berhasi dihapus')
            self.secondcanvas.delete(vtag)
            self.secondcanvas.delete('li'+vtag)
            self.secondcanvas.delete('lo'+vtag)
            self.secondcanvas.delete('lbi'+vtag)
            self.secondcanvas.delete('lbo'+vtag)
            # self.lineNum = len(self.secondcanvas.find_withtag('line'))+1
        
    # Fungsi untuk delete line 
    def delLine(self,x,y,linetag):
        if linetag != False:
            self.log('Line '+str(linetag)+' berhasil dihapus')
            self.secondcanvas.delete(self.secondcanvas.find_withtag(linetag)[0]+1)
            self.secondcanvas.delete(linetag)
            # self.lineNum-=1

    # Fungsi untuk cek apakah klikan mouse berada diatas objek atau tidak
    # kalau iya, ia akan return tag objek yg bersinggungan
    # kalau tidak, return false
    def isIntersect(self, x, y,obj='circle'):
        allver = self.secondcanvas.find_withtag(obj)
        # self.log('current pos '+str(x)+' '+str(y))
        # self.log(self.mode)
        if obj == 'circle':
            for i in allver:
                x1,y1,x2,y2 = self.secondcanvas.coords(i)
                if x>=x1 and y >= y1 and x<=x2 and y<=y2:
                    vtag = self.secondcanvas.gettags(i)[0]
                    return vtag
                # self.log(str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2))
        elif obj == 'line':
            for i in allver:
                x1,y1,x2,y2 = self.secondcanvas.coords(i)

                #cek line vertikal kah?
                if (x1==x2 or x==x1 or x==x2):
                    if self.isBetween(x,y,x1,y1,x2,y2):
                        # self.log('Vertical Line !!')
                        linetag = self.secondcanvas.gettags(i)[0]
                        return linetag
                else:
                    grad = abs((y2-y1)/(x2-x1))
                    gradcek = abs((y-y1)/(x-x1))
                    offset = 0.06

                    # self.log(str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2))
                    # self.log('gradient asli = '+str(grad))
                    # self.log('gradient cek = '+str(gradcek))

                    if self.isBetween(x,y,x1,y1,x2,y2) and grad-offset<=gradcek and gradcek <= grad+offset:
                        linetag = self.secondcanvas.gettags(i)[0]
                        return linetag
                # self.log('not intersect w line')

        return False
    
    def isBetween(self,x,y,x1,y1,x2,y2):
        if (x1<=x and x<=x2) and (y1<=y and y<=y2):
            # self.log('isBetween 1')
            return True
        elif (x2<=x and x<=x1) and (y2<=y and y<=y1):
            # self.log('isBetween 2')
            return True
        elif (x1<=x and x<=x2) and (y2<=y and y<=y1):
            # self.log('isBetween 3')
            return True
        elif (x2<=x and x<=x1) and (y1<=y and y<=y2):
            # self.log('isBetween 4')
            return True
        # self.log('not in between !')
        return False

    def delAll(self, *args):
        self.secondcanvas.delete("all")
        self.log('',True)
        self.vertexNum = 1
        self.lineNum = 1
        self.currentvertex = False

    def getComboVal(self):
        return self.dropval.get()


    def backmenormal(self):
        if self.mode=='run':
            self.secondcanvas.itemconfigure('line',fill='blue')
            self.idx+=1
            for i in range(0,self.idx):
                try:
                    self.secondcanvas.itemconfigure(self.linesaver[i],fill='green')
                except IndexError:
                    # self.log('backmenormal done')
                    # self.stop()
                    pass
            self.log("Adding new possible edges(if any)")
    
    def greenmein(self):
        if self.mode=='run':
            try:
                self.secondcanvas.itemconfigure(self.linesaver[self.idx],fill='green')
            except IndexError:
                pass
            for i in range(0,len(self.vertice)):
                if(self.idx==self.vertice[i]):
                    self.log('Selected Line causing Loop!')
                    break
                elif(i+1>=len(self.vertice)):
                    self.log("Found!")
            # self.lines.pop(0)
            self.secondcanvas.after(1000,self.backmenormal)

    def animateprim(self):
        if self.mode=='run':
            self.lines=[]
            try:
                nextstep=self.animatedprim.pop(0)
                for i in range(0,len(nextstep)):
                    self.lines.append(nextstep[i])
                llen=len(self.lines)
                self.linecolor='yellow'
                # print(self.lines)
                self.log("Sorting Process")
                self.showline()
                # self.lines.append(self.linesaver[self.idx])
                
                self.secondcanvas.after(1000*(llen),self.greenmein)
                self.secondcanvas.after(1000*(llen+2),self.animateprim)
            except IndexError:
                self.log('Prims Selesai !')
                # self.stop()
                pass

    def animatedjikstra(self):
        if(self.mode=='run'):
            try:
                # tag=self.myobject.GetMyVertexAt(self.idx).GetIdx()
                weight=self.vertice.pop(0)
                # print(weight)
                # self.log('Exploring possible route to search the sortest path to each vertex')
                self.log('Update '+str(weight[1])+"'s distance!")
                self.log("Adding new possible vertex!")
                self.secondcanvas.itemconfigure('w'+str(weight[1]),text=str(weight[0]))
                self.secondcanvas.itemconfigure('line',fill='blue')
                nextroute=self.linesaver.pop(0)
                self.idx+=1
                # self.log("")
                for i in nextroute:
                    self.secondcanvas.itemconfigure(i,state='normal',fill='yellow')
                self.secondcanvas.after(1000,self.animatedjikstra)
            except IndexError:
                self.secondcanvas.itemconfigure('line',fill='blue')
                self.showline()

    def showline(self):
        if self.mode == 'run':
            comboval = self.getComboVal()
            try:
                nextline=self.lines.pop(0)
                # self.log(nextline)
                self.secondcanvas.itemconfigure(nextline,state='normal',fill=self.linecolor)
                self.secondcanvas.after(1000,self.showline)
            except IndexError:
                if comboval == 'Prims':
                    self.log('Tampilkan Line !')
                else:
                    self.log(comboval+' Selesai !')
                # self.stop()
                pass
    
    def showvertex(self):
        if self.mode=='run':
            try:
                nextvertex=self.lines.pop(0)
                nextcolor=self.vertice.pop(0)
                warna=0
                if(nextcolor[1]==0):
                    #red
                    warna='red'
                elif(nextcolor[1]==1):
                    #green
                    warna='green'
                elif(nextcolor[1]==2):
                    #blue
                    warna='#0400FF'
                elif(nextcolor[1]==3):
                    #yellow
                    warna='#FFFF00'
                elif(nextcolor[1]==4):
                    #purple
                    warna='#9D00FF'
                elif(nextcolor[1]==5):
                    #orange
                    warna='#FF7F00'
                elif(nextcolor[1]==6):
                    #silver
                    warna='#C1C1C1'
                elif(nextcolor[1]==7):
                    #white
                    warna='#FFFFFF'
                elif(nextcolor[1]==8):
                    #black
                    warna='#000000'
                else:
                    warna=nextcolor[1]
                self.secondcanvas.itemconfigure(nextvertex,fill=warna,outline=warna)
                self.secondcanvas.after(1000,self.showvertex)
            except IndexError:
                self.log('Coloring Selesai !')
                # self.stop()
                pass

    def rgb2hex(self,r,g,b):
        hex = "#{:02x}{:02x}{:02x}".format(r,g,b)
        return hex

    def run(self, *args):
        if self.mode == 'add' or self.mode == 'edit':
            self.beforeRunMode = self.mode
            self.mode = 'run'
            self.idx=0
            self.lines=[]
            self.vertice=[]
            self.linesaver=[]
            self.btnRun.configure(state='disabled')
            self.btnAdd.configure(state='disabled')
            self.btnEdit.configure(state='disabled')
            self.btnClear.configure(state='disabled')
            self.btnRandom.configure(state='disabled')
            self.btnStop.configure(state='normal')
            self.btnAbout.configure(state='disabled')
            comboval = self.getComboVal()
            self.myobject.DelMyVertexAll()
            self.myobject.DelMyLineAll()
            self.myobject.DelMyMstAll()
            allvertex = self.secondcanvas.find_withtag('circle')
            alllines = self.secondcanvas.find_withtag('line')
            vertexnya=[]
            ### 2 for dibawah gae opo ? ###
            # Buat komputasi, kan butuh data line nya terhubung vertex apa aja
            # beratnya berapa
            # object vertex ga terlalu berguna kalau ndak ada fitur random jumlah vertex & line
            for i in allvertex:
                currentvertextag = self.secondcanvas.gettags(i)
                vertexholder = Vertex()
                # print(currentvertextag)
                vertexholder.SetTag(currentvertextag)
                vertexholder.SetIdx(int(currentvertextag[0][1:]))
                vertexnya.append(vertexholder.GetIdx())
                self.myobject.PushMyVertex(vertexholder)

            if(self.myobject.GetMyVertexSize()==0):
                messagebox.showwarning("Error occured!","Tidak ada vertex!")
                return

            for i in alllines:
                currentlinetag = self.secondcanvas.gettags(i)
                # print(currentlinetag)
                lineholder = Line()
                lineholder.SetWeight(int(currentlinetag[4]))
                lineholder.SetTag(currentlinetag)
                lineholder.SetVAll((int(currentlinetag[1][3:]),int(currentlinetag[3][3:])))
                self.myobject.PushMyLine(lineholder)
            

            note=1
            if comboval == 'Djikstra':
                self.log('Running Djikstra !')
                self.popWindow(labeltext="Masukkan titik keberangkatan vertex :")
                self.wait_window(self.top) #self.top -> variable yg menyimpan object popwindow / dialog
                start=self.popvalue #popvalue itu yang nyimpan valuenya
                self.popWindow(labeltext="Masukkan titik tujuan vertex :",popvalue=2)
                self.wait_window(self.top)
                end=self.popvalue
                # self.vertice.append((0,start))
                if(self.myobject.GetMyLineSize()==0):
                    return #kalau gak ada line nya ndak ada yg harus di-compute
                # self.secondcanvas.itemconfigure('line',state='hidden')
                process=self.myobject.Compute('Djikstra',val1=start,val2=end)
                for i in allvertex:
                    x,y,x1,y1=self.secondcanvas.coords(i)
                    tag=self.secondcanvas.gettags(i)
                    self.secondcanvas.create_text(x+20,y-15,text="-",font=(200),tags=('w'+str(tag[0][1:]),'weight'),fill='blue')
                self.secondcanvas.itemconfigure('w'+str(start),text=str(0))
                for i in range(0,len(process)):
                    routehold=process[i][1]
                    routeme=[]
                    for j in range(0,self.myobject.GetMyLineSize()):
                        lholder=self.myobject.GetMyLineAt(j)
                        v=lholder.GetVend()
                        w=lholder.GetVstart()
                        ltag=lholder.GetTag()
                        lobj=self.secondcanvas.find_withtag(ltag[0])
                        # print(process[i])
                        # print(str(v)+" "+str(w))
                        if(len(routehold)-1!=0):
                            for k in range(0,len(routehold)-1):
                                if(v==routehold[k] and w == routehold[k+1]):
                                    routeme.append(lobj)
                                    # print("-"+ str(ltag))
                                elif(v==routehold[k+1] and w ==routehold[k]):
                                    routeme.append(lobj)
                                    # print("-"+str(ltag))
                        if(process[i][0]==v and process[i][2]==w):
                            routeme.append(lobj)
                            # print(ltag)
                        elif(process[i][0]==w and process[i][2]==v):
                            routeme.append(lobj)
                            # print(ltag)
                    # print(routehold)
                    # print("----")
                    # print(process[i])
                    #kari update bobote
                    self.vertice.append((process[i][3],process[i][2])) 
                    self.linesaver.append(routeme)

                self.animatedjikstra()
                # self.secondcanvas.itemconfigure('line',fill='blue')

            elif comboval == 'Prims':
                self.log('Running Prims !')
                if(self.myobject.GetMyLineSize()==0):
                    return #kalau gak ada line nya ndak ada yg harus di-compute
                self.popWindow(labeltext='Masukkan sembarang Vertex')
                self.wait_window(self.top)

                completed=False
                while(not completed):
                    for i in range(0,len(vertexnya)):
                        if (self.popvalue==vertexnya[i]):
                            completed=True
                            break
                    if(not completed):
                        messagebox.showwarning("Error Occured", "Vertex tidak ada!")
                        self.popWindow(labeltext='Masukkan sembarang Vertex')
                        self.wait_window(self.top)

                pholder=self.myobject.Compute('Prims',val1=self.popvalue ,val2=self.vertexNum+1)
                animatedprims=pholder[0]
                self.vertice=pholder[1]
                for i in range(0,len(animatedprims)):
                    self.animatedprim.append([])
                    for j in range(0,len(animatedprims[i])):
                        vholder=animatedprims[i][j]
                        for k in range(0,self.myobject.GetMyLineSize()):
                            curobj=self.myobject.GetMyLineAt(k)
                            realobj=self.secondcanvas.find_withtag(curobj.GetTag()[0])
                            if(vholder[0]==curobj.GetVend() and vholder[1]==curobj.GetVstart()):
                                # realobj=self.secondcanvas.find_withtag(curobj.GetTag()[0])
                                self.animatedprim[i].append(realobj)
                                break
                            elif(vholder[1]==curobj.GetVend() and vholder[0]==curobj.GetVstart()):
                                self.animatedprim[i].append(realobj)
                                break
                    #     print(vholder)
                    # print(self.animatedprim[i])
                    # print("----")

            elif comboval == 'Kruskal':
                self.log('Running Kruskal !')
                self.log("1. Sorting Edge berdasarkan beratnya!")
                self.log("2. Pilih Edge satu-persatu dari yang paling kecil tanpa Loop")
                if(self.myobject.GetMyLineSize()==0):
                    return #kalau gak ada line nya ndak ada yg harus di-compute
                cycliclist = self.myobject.Compute('Kruskal',val1=self.vertexNum)
                for i in range(0,self.myobject.GetMyLineSize()):
                    lholder=self.myobject.GetMyLineAt(i)
                    if(len(cycliclist)!=0 and i == cycliclist[0]):
                        cycliclist.pop()
                        self.log(str(lholder.GetVstart())+" - "+str(lholder.GetVend())+" : "+ str(lholder.GetTag()[4]) + " Rejected - Loop!")
                    else:
                        self.log(str(lholder.GetVstart())+" - "+str(lholder.GetVend())+" : "+ str(lholder.GetTag()[4]) + " Accepted!")
            elif comboval == 'Naive Coloring':
                self.log('Running Naive Coloring !')
                # self.log("")
                colored=self.myobject.Compute('GColor',val1=self.vertexNum)
                note=2
            elif comboval == 'Fuery':
                self.log("Running Feury")
                self.log("Eulerian Path is a path in graph that visits every edge exactly once. Eulerian Circuit is an Eulerian Path which starts and ends on the same vertex.")
                self.log("===================")
                self.log("Feury Algorithm is to find the track of that path or circuit")
                self.log("More about the algorithm on https://www.geeksforgeeks.org/fleurys-algorithm-for-printing-eulerian-path/\n")
                
                if(self.myobject.Compute('Feury',val1=self.vertexNum)==False):
                    self.log("Perhatikan bahwa didalam algoritma ini mempunyai 'arah'")
                    note=0
                # self.log('Fuery Run !')
            elif comboval =='N Max Coloring':
                self.log("Running N Max Coloring")
                self.popWindow(labeltext='Masukkan jumlah maksimal warna!',popvalue=3)
                self.wait_window(self.top)
                nColour=self.popvalue
                colored=self.myobject.Compute('BColor',val1=self.vertexNum,val2=nColour)
                for i in range(1,len(colored)):
                    if(colored[i][1]!=colored[i-1][1]):
                        break
                    elif(i+1>=len(colored)):
                        if(self.myobject.GetMyLineSize()!=0):
                            note=99
                            self.log("Tidak bisa menemukan kombinasi warna-nya!")
                            self.stop()
                if(not colored):
                    note=99
                    #kasih warning
                    self.log("Tidak bisa menemukan kombinasi warna-nya!")
                    self.stop()
                else:
                    note=2
            #masukin hasil komputasi ke queue line yg akan ditampilkan
            if(note==1):
                for i in range(0,self.myobject.GetMyMstSize()):
                    holder=self.myobject.GetMyMstAt(i)
                    if(holder!='salah'):
                        linetag=holder.GetTag()
                        obj=self.secondcanvas.find_withtag(linetag[0])
                    self.lines.append(obj)
                if(comboval!='Prims'):
                    if(comboval!='Djikstra'):
                        self.showline()
                else:
                    self.linesaver=self.lines
                    self.animateprim()
            elif(note==2):
                # morecolor=[[]]*self.vertexNum
                if(self.myobject.GetMyVertexSize()<=8):
                    for i in range(0,self.myobject.GetMyVertexSize()):
                        holder=self.myobject.GetMyVertexAt(i)
                        #reuse line untuk menyimpan objek vertex
                        #simpan warnanya di vertice
                        vtag=holder.GetTag()
                        # print(vtag)
                        vholder=self.secondcanvas.find_withtag(vtag[0])
                        self.lines.append(vholder[0])
                        self.vertice.append(colored[holder.GetIdx()])
                    # print(colored)
                else:
                    # print(colored)
                    morecolor=[]
                    for i in range(0,self.vertexNum+1):
                        morecolor.append([])
                    for i in range(0,self.myobject.GetMyVertexSize()):
                        holder=self.myobject.GetMyVertexAt(i)
                        vtag=holder.GetTag()
                        # vholder=self.secondcanvas.find_withtag(vtag[0])
                        # print(holder.GetIdx())
                        # print(colored[holder.GetIdx()])
                        cholder=colored[holder.GetIdx()]
                        morecolor[cholder[1]].append(holder.GetIdx())
                        #warna ke x append indexnya 
                        #kayak 'bak' / dikumpulin id vertex sesuai warna
                        # print(morecolor)
                    for i in range(0,self.vertexNum):
                        r=random.randint(0,255)
                        g=random.randint(0,255)
                        b=random.randint(0,255)
                        output=self.rgb2hex(r,g,b)
                        for j in range(0,len(morecolor[i])):
                            colored[morecolor[i][j]]=(True,output)
                    
                    for i in range(0,self.myobject.GetMyVertexSize()):
                        holder=self.myobject.GetMyVertexAt(i)
                        vtag=holder.GetTag()
                        vholder=self.secondcanvas.find_withtag(vtag[0])
                        self.lines.append(vholder[0])
                        self.vertice.append(colored[holder.GetIdx()])                   
                self.showvertex()
            elif(note==0):
                self.log("Graf yang diberikan bukan 'Eulerian Graph' karena memiliki lebih dari 2 vertex yang berderajat ganjil.")
                self.stop()
            # self.log("Computation Ended")
            # self.stop()

    def stop(self,*args):
        if self.mode == 'run':
            self.secondcanvas.delete('weight')
            self.secondcanvas.itemconfigure('line',state='normal',fill='blue')
            self.btnRun.configure(state='normal')
            if self.beforeRunMode == 'add':
                self.btnEdit.configure(state='normal')
            else:
                self.btnAdd.configure(state='normal')
            self.btnClear.configure(state='normal')
            self.btnRandom.configure(state='normal')
            self.btnStop.configure(state='disabled')  
            self.btnAbout.configure(state='normal')          
            allvertex = self.secondcanvas.find_withtag('circle')
            for i in allvertex:
                self.secondcanvas.itemconfigure(i,fill="#00BCD4",outline='#0097A7')
            self.mode=self.beforeRunMode

    def addMode(self,*args):
        if self.mode == 'edit':
            self.mode = 'add'
            self.log(self.mode+' mode on')
            self.btnAdd.configure(state='disabled')
            self.btnEdit.configure(state='normal')
  

    def editMode(self,*args):
        if self.mode == 'add':
            self.mode = 'edit'
            self.log(self.mode+' mode on')
            self.btnAdd.configure(state='normal')
            self.btnEdit.configure(state='disabled')

    def about(self,*args):
        
        win = tk.Toplevel(padx=30 , pady=10, width=2000)
        win.title('About Theory Graph is Fun')
        msg = """Made with ❤ by:
    Akbar Noto (16-028)
    Ayas Faikar Nafis (16-138)
        """
        ttk.Label(win, text=msg).pack()
        ttk.Button(win, text='Ok', command=win.destroy).pack(side='left')
        new = 1
        url = "https://github.com/abaar/regrafit"
        ttk.Button(win, text='Github', command=lambda:webbrowser.open(url,new=new)).pack(side='right')


    def randomVertex(self,*args):
        self.log("Generating graph !")
        self.delAll()
        totalVertex=random.randint(6,10)
        occupied=[]
        for i in range(0,12):
            occupied.append([])
            for j in range(0,12):
                occupied[i].append(False)
        #buat simpen di titik i,j udah ada vertexnya belum
        r=20
        coords=[]
        coords.append((0,0))
        for i in range(0,totalVertex):
            x=random.randint(1,10)
            y=random.randint(1,5)
            while(occupied[x][y]):
                x=random.randint(1,10)
                y=random.randint(1,5)
            occupied[x][y]=True
            x=x*70
            y=y*90
            #random 1-10 trus dikalikan pixel nya biar estetik
            #kan 720x480
            coords.append((x,y))
            self.secondcanvas.create_oval(x+r, y+r, x-r,y-r,fill="#00BCD4", outline="#0097A7", width=2, tags=('v'+str(self.vertexNum),'circle','vertex'))
            self.secondcanvas.create_text(x,y,text=str(self.vertexNum), font=(200), tags=('v'+str(self.vertexNum),'label','vertex'))
            self.vertexNum=self.vertexNum+1            
        
        threedegree=random.randint(1,2)
        vertexdegree=[0]*(self.vertexNum)
        occupied=[]
        for i in range(0,self.vertexNum):
            occupied.append([])
            for j in range(0,self.vertexNum):
                occupied[i].append(False)
        #buat ngecek i->j udah ada line nya blm , vice versa

        prev=0
        for i in range(0,threedegree):
            three=random.randint(1,self.vertexNum-1)
            while(threedegree>1 and prev==three):
                three=random.randint(1,self.vertexNum-1)
            vertexdegree[three]=3
            xvertex,yvertex = coords[three] #coords from
            for j in range(0,3):
                target=random.randint(1,self.vertexNum-1)
                #kalau sama / three->target udah ada line / degree target >=3 cari lagi
                while(target==three or occupied[three][target] or occupied[target][three] or vertexdegree[target]>=3):
                    target=random.randint(1,self.vertexNum-1)
                    #jadi selama dia udah keipilih random terus
                occupied[three][target]=True
                occupied[target][three]=True
                vertexdegree[target]+=1
                xtvertex,ytvertex=coords[target] #coords target
                weig=random.randint(1,50)
                line=self.secondcanvas.create_line((xvertex,yvertex,xtvertex,ytvertex),fill='blue',width=3,tags=('ln'+str(self.lineNum),'lov'+str(three),'line','liv'+str(target),str(weig)))
                linecoord = self.secondcanvas.coords('ln'+str(self.lineNum))
                xLineLabel = (linecoord[0]+linecoord[2])/2
                yLineLabel = (linecoord[1]+linecoord[3])/2
                self.secondcanvas.create_text(xLineLabel,yLineLabel,text=str(weig), font=(200), tags=('lb'+str(self.lineNum),'label','lbov'+str(three),'lbiv'+str(target)))
                self.lineNum+=1
                self.secondcanvas.tag_lower(line)

        #nah disini untuk yg belum kena degree
        #counter=0
        zerovertex=[]
        for i in range(1,len(vertexdegree)):
            if(vertexdegree[i]==0):
                zerovertex.append(i)
        counter=len(zerovertex)

        if(totalVertex-counter>=2):
            fullgraph=random.randint(0,1)
            for i in range(0,totalVertex-counter-fullgraph):
                try:
                    start=zerovertex.pop(0)
                    xvertex,yvertex=coords[start]
                    target=random.randint(1,self.vertexNum-1)
                    while(occupied[start][target] or occupied[target][start] or start==target):
                        target=random.randint(1,self.vertexNum-1)
                    xtvertex,ytvertex=coords[target]
                    occupied[start][target]=True
                    occupied[target][start]=True
                    weig=random.randint(1,50)
                    line=self.secondcanvas.create_line((xvertex,yvertex,xtvertex,ytvertex),fill='blue',width=3,tags=('ln'+str(self.lineNum),'lov'+str(start),'line','liv'+str(target),str(weig)))
                    linecoord = self.secondcanvas.coords('ln'+str(self.lineNum))
                    xLineLabel = (linecoord[0]+linecoord[2])/2
                    yLineLabel = (linecoord[1]+linecoord[3])/2
                    self.secondcanvas.create_text(xLineLabel,yLineLabel,text=str(weig), font=(200), tags=('lb'+str(self.lineNum),'label','lbov'+str(start),'lbiv'+str(target)))
                    self.lineNum+=1
                    self.secondcanvas.tag_lower(line)
                except IndexError:
                    pass
        # self.log("Total vertex :" + str(self.vertexNum))