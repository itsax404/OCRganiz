import tkinter as tk
class Liste_interface (tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.list_file = [] # création de la liste avec toutes les adresses des fichiers
    def affichage(self):
        self.label = tk.Label(master=self.file_frame, text="classe test")
        self.label.pack()

def affichagetest(master):
    label = tk.Label(master=master, text="classe test")
    label.pack()