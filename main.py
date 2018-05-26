from gui import Gui
import tkinter as tk

if (__name__ == "__main__"):
    root = tk.Tk()
    root.title("Graph Theory is Fun")
    app = Gui(master=root)
    app.mainloop()
