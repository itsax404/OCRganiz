import tkinter as tk
from tkinter import ttk
import os.path


class List_selection_rect(tk.Frame):
    def __init__(self, master: tk.Frame, type: str):
        """
        Création d'une liste dynamique
        qui change ces valeurs en fonction du type
        :param master: Frame Parent
        :param type: type de fichier
        """
        super().__init__(master)
        self.master = master
        self.grid(row=3, column=0)
        self.type = type
        self.parent_dir = os.path.join(os.path.realpath(__file__), os.pardir, os.pardir, os.pardir)

    def affichage(self) -> None:
        """
        Affichage de toute la liste
        :return: None
        """
        self.tree = ttk.Treeview(master=self.master)
        self.tree.heading('#0', text='Zone de données importantes', anchor=tk.W)

        self.update_tree()
        self.tree.grid(row=3, column=0, padx=10)

    def update_tree(self) -> None:
        """
        Recharge la liste avec les lignes et les sous-lignes:
        -ligne 1
            -sousligne 1
        :return: None
        """
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
                        iid = dict_modele[nom_ligne] + "." + tabchildren[j]
                        self.tree.insert('', tk.END, text=tabchildren[j], iid=iid, open=False)
                        self.tree.move(iid, dict_modele[nom_ligne], j)
                nom_souschildren = f"subsubligne {i}"
                if nom_souschildren in dict_modele:
                    tabsouschildren = dict_modele[nom_souschildren]
                    for k in range(0, len(tabsouschildren)):
                        idd_parent = dict_modele[nom_ligne] + "." + tabchildren[j]
                        iid = dict_modele[nom_ligne] + "." + tabchildren[j] + "." + tabsouschildren[k]
                        self.tree.insert('', tk.END, text=tabsouschildren[k], iid=iid, open=False)
                        self.tree.move(iid, idd_parent, k)

    def get_tree_modele(self) -> None:
        """
        Récupérer les paramètres dans le fichier 'Type_tree'
        :return: None
        """
        type_path = os.path.join(self.parent_dir, "Config_interface", 'Type_tree')
        fichier = open(type_path, "r")
        tree_type = fichier.readlines()
        fichier.close()
        modele_trouve = False
        i = 0
        for ligne in tree_type:

            if ligne.find(self.type) != -1:
                modele_trouve = True
            if (modele_trouve == True and ligne.find("{") != -1):
                debut = i
            if (modele_trouve == True and ligne.find("}") != -1):
                fin = i
                break
            i += 1
        dict = ""
        for x in range(debut, fin + 1):
            dict += tree_type[x]
        dict = eval(dict.replace("'", "\""))
        return dict

    def set_type(self, type: str) -> None:
        """
        :param type: Type du fichier
        :return: None
        """
        self.type = type

    def get_selection_id(self) -> str:
        """
        Permets de récupérer l'identifiant de la ligne sélectionner
        :return: id correspondant à la selection de l'utilisateur
        """
        if len(self.tree.selection()) != 0:
            selected_item = self.tree.selection()[0]
            if self.tree.parent(selected_item) == "":
                parent_id = selected_item
            else:
                parent_id = self.tree.parent(selected_item)
            if parent_id not in ["personne", "adresse", "entreprise"]:
                id = selected_item + "." + "flottant"
                return id
            elif parent_id != "":
                id = selected_item
                return id
