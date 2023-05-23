import tkinter as tk
from tkinter import ttk, messagebox
class Liste_interface (tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
    def affichage(self):

        self.frame = tk.Frame(master=self.master, borderwidth=5, relief="ridge")
        self.frame.pack(fill=tk.BOTH)

        self.file_btn = tk.LabelFrame(self.frame, text="test")
        self.file_btn.pack(fill=tk.BOTH, padx=10)

        self.file_frame = tk.LabelFrame(self.frame, text="liste des fichiers")
        self.file_frame.pack(fill=tk.BOTH, padx=10)

        btn_all = tk.Button(master=self.file_btn, text="Selectionner tout les fichiers", command=self.tout_select)
        btn_all.grid(row=0, column=0, padx=10)

        btn_suppr = tk.Button(master=self.file_btn, text="supprimer", command=self.suppr)
        btn_suppr.grid(row=0, column=1, padx=10)

        btn_visualisation = tk.Button(master=self.file_btn, text="visualiser fichier", command=self.visualisation)
        btn_visualisation.grid(row=0, column=2, padx=10)

        self.tv = ttk.Treeview(master=self.file_frame, columns=(1, 2, 3), show='headings', height=3)
        self.tv.grid(pady=10, padx=10, row=1, column=0)

        self.tv.column(1, width=25)
        self.tv.column(2, width=575)
        self.tv.column(3, width=50)

        self.tv.heading(1, text='Type')
        self.tv.heading(2, text='Adresse du fichier')
        self.tv.heading(3, text='date')

        style = ttk.Style()
        style.theme_use("default")
        style.map("Treeview")

        scrollbar = tk.Scrollbar(self.file_frame)
        scrollbar.grid(row=1, column=3)

        self.tv.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tv.yview)



    def add(self, file):
        if(file!=None) :
            for newfile in file:
                self.tv.insert(parent='', index='end', values=(0, newfile, 5))

    def suppr(self):
        res = messagebox.askyesno('', 'Voulez-vous vraiment supprimer les fichers?')
        if res == True:
            for selected_item in self.tv.selection():
                self.tv.delete(selected_item)


    def tout_select(self):
        """
        TODO docstring
        :return:
        """
        for item in self.tv.get_children():
            self.tv.selection_add(item)

    def visualisation(self):
        selected_item = self.tv.selection()[0]
        v_fenetre = visualisation_pdf(self.master)
        v_fenetre.affichage()
class visualisation_pdf (tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Visual pdf")
        self.geometry("800x800")
    def affichage(self):
        label = tk.Label(master=self, text="thomas")
        label.pack()


