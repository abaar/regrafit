import tkinter as tk
from tkinter import ttk

lines = []

def showNextLine():
    global lines
    try:
        nextLine = lines.pop(0)
        canvas.itemconfigure(nextLine[0],state='normal')
        root.after(1000,showNextLine)
    except IndexError:
        pass
        #No more items in list.

root = tk.Tk()
canvas = tk.Canvas()
canvas.grid()
canvas.create_line((50,50,100,100),fill='red',tags=('line1','line'),state='normal')
canvas.create_line((50,60,100,110),fill='blue',tags=('line2','line'),state='normal')
canvas.create_line((50,70,100,120),fill='yellow',tags=('line3','line'),state='normal')
canvas.create_line((50,80,100,130),fill='green',tags=('line4','line'),state='normal')

#lines = list(canvas.find_withtag('line'))

root.after(1500,canvas.itemconfigure('line',state='hidden'))

alllines = canvas.find_withtag('line')
for i in alllines:
	lines.append(canvas.gettags(i))
print(type(lines),lines)
root.after(1000,showNextLine)
root.mainloop()

root.mainloop()