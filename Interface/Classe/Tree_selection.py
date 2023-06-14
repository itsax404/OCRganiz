import tkinter as tk
from tkinter import ttk
class List_selection_rect (tk.Frame):
    def __init__(self, master, modele):
        super().__init__(master)
        self.master = master
        self.grid()
        self.modele = modele


    def affichage(self):
        self.tree = ttk.Treeview(master=self.master)
        self.tree.heading('#0', text='Zone de données importantes', anchor=tk.W)

        self.update_tree()
        self.ajouter_parent("parent1")
        self.tree.grid(row=1, column=1, padx=10)


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
        fichier = open("C:\\Users\\thoma\\PycharmProjects\\projet-programmation\\test\\tree_modèle", "r")
        tree_modele = fichier.readlines()
        fichier.close()
        modele_trouve = False
        i = 0
        for ligne in tree_modele:

            if ligne.find(self.modele) != -1:
                modele_trouve = True
            if (modele_trouve == True and ligne.find("{") != -1):
                debut = i
                print(debut)
            if (modele_trouve == True and ligne.find("}") != -1):
                fin = i
                print(fin)
                break
            i += 1
        dict=""
        for x in range(debut, fin+1):
            dict += tree_modele[x]
        dict = eval(dict.replace("'", "\""))
        return dict

    def set_modele(self, newmodele):
        self.modele = newmodele
        print(self.modele)


    def ajouter_parent(self, id_parent):
        self.tree.insert('', tk.END, text=id_parent, iid=id_parent, open=False)


    def ajouter_enfant(self, id_enfant):
        self.tree.insert('', tk.END, text=id_enfant, iid=id_enfant, open=False)
        selected_parent = self.tree.selection()[0]
        print(self.tree.parent(selected_parent))
        #self.tree.move(id_enfant, selected_parent,)