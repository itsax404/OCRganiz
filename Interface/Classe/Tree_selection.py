import tkinter as tk
from tkinter import ttk
import os.path
class List_selection_rect (tk.Frame):
    def __init__(self, master, modele):
        super().__init__(master)
        self.master = master
        self.grid(row=3, column=0)
        self.modele = modele
        self.parent_dir = os.path.join(os.path.realpath(__file__), os.pardir, os.pardir, os.pardir)


    def affichage(self):
        self.tree = ttk.Treeview(master=self.master)
        self.tree.heading('#0', text='Zone de données importantes', anchor=tk.W)

        self.update_tree()
        self.tree.grid(row=3, column=0, padx=10)


    def update_tree(self):
        for selected_item in self.tree.get_children():
            self.tree.delete(selected_item)
        dict_modele = self.get_tree_modele()
        nb_ligne = len(dict_modele)
        for i in range(0, nb_ligne):
            nom_ligne = f"ligne {i}"
            if nom_ligne in dict_modele:
                self.tree.insert('', tk.END, text=dict_modele[nom_ligne], iid=dict_modele[nom_ligne], open=False)
                nom_children = f"subligne {i}"
                if nom_children in dict_modele:
                    tabchildren = dict_modele[nom_children]
                    for j in range(0, len(tabchildren)):
                        self.tree.insert('', tk.END, text=dict_modele[nom_children][j], iid=dict_modele[nom_children][j], open=False)
                        self.tree.move(dict_modele[nom_children][j], dict_modele[nom_ligne], j)



    def get_tree_modele(self):
        type_path = os.path.join(self.parent_dir, "Config_interface","Type", 'Type_tree')
        fichier = open(type_path, "r")
        tree_type = fichier.readlines()
        fichier.close()
        modele_trouve = False
        i = 0
        for ligne in tree_type:

            if ligne.find(self.modele) != -1:
                modele_trouve = True
            if (modele_trouve == True and ligne.find("{") != -1):
                debut = i
            if (modele_trouve == True and ligne.find("}") != -1):
                fin = i
                break
            i += 1
        dict=""
        for x in range(debut, fin+1):
            dict += tree_type[x]
        dict = eval(dict.replace("'", "\""))
        return dict


    def set_modele(self, newmodele):
        self.modele = newmodele


    def get_selection_id(self):
        if self.tree.selection() != ():
            selected_item = self.tree.selection()[0]
            parent_id = self.tree.parent(selected_item)
            if parent_id != "":
                id = parent_id + "." + selected_item
                return tuple((parent_id, id))

            else:
                id = selected_item
                return tuple((id, None))