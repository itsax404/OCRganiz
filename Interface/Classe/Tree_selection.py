import tkinter as tk
class Liste_interface_c (tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
    def affichage(self):
