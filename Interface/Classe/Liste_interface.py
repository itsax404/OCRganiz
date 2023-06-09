import tkinter as tk
from backend.database import Database
from backend.images.image_processor import Image_Processor
from tkinter import ttk, messagebox, Menu, filedialog
from .PdFviewer import Visualisation_pdf
from .Fenetre_def_modèle import Defenir_modele
from backend.enregistrement import enregistrer


class Liste_interface_c(tk.Frame):
    def __init__(self, master: tk.Frame, main_path: str, database: Database, image_processor: Image_Processor):
        """
        Initialisation de la list qui gère les pdf: type, adresse du fichier, modèle
        :param master: Frame où la liste sera afficher
        :param main_path: Dossier racine du programme
        :param database: Base de données
        :param image_processor:
        """
        super().__init__(master)
        self.master = master
        self.pack(side="top")
        self.path = main_path
        self.database = database
        self.image_processor = image_processor

    def affichage(self) -> None:
        """
        Affichage de la liste et des butons pour gerer cette dernière
        :return: None
        """

        self.frame = tk.Frame(master=self.master, borderwidth=5, relief="ridge")
        self.frame.pack(side="top")

        self.affichage_label_btn()

        self.affichage_label_list()

    def affichage_label_btn(self) -> None:
        """Affichage des butons : tout selectonner, supprimer et visualiser .
            Returns: None"""

        self.file_btn = tk.LabelFrame(self.frame, text="Option")
        self.file_btn.pack(fill=tk.BOTH, padx=20, pady=10)

        btn_all = tk.Button(master=self.file_btn, text="Sélectionner tout les fichiers", command=self.tout_select)
        btn_all.grid(row=0, column=0, padx=10, pady=10)

        btn_suppr = tk.Button(master=self.file_btn, text="Supprimer", command=self.suppr)
        btn_suppr.grid(row=0, column=1, padx=10, pady=10)

        btn_visualisation = tk.Button(master=self.file_btn, text="Visualiser fichier", command=self.visualisation)
        btn_visualisation.grid(row=0, column=2, padx=10, pady=10)

        btn_visualisation = tk.Button(master=self.file_btn, text="Définir modèle", command=self.open_fenetre_modèle)
        btn_visualisation.grid(row=0, column=3, padx=10, pady=10)

        btn_visualisation = tk.Button(master=self.file_btn, text="Insérer", command=self.inserer_bdd)
        btn_visualisation.grid(row=0, column=4, padx=10, pady=10)

    def affichage_label_list(self) -> None:

        """
        Affichage de la liste des fichiers + scrollbar pour defiler les fichiers insérés
        :return: None
        """
        "frame"
        self.file_frame = tk.LabelFrame(self.frame, text="liste des fichiers")
        self.file_frame.pack(fill=tk.BOTH, padx=10)

        # liste
        self.tv = ttk.Treeview(master=self.file_frame, columns=(1, 2, 3), show='headings', height=30)
        self.tv.grid(pady=10, padx=10, row=1, column=0)

        self.tv.column(1, width=25)
        self.tv.column(2, width=575)
        self.tv.column(3, width=50)

        self.tv.heading(1, text='Type')
        self.tv.heading(2, text='Adresse du fichier')
        self.tv.heading(3, text='Modèle')

        style = ttk.Style()
        style.theme_use("default")
        style.map("Treeview")
        #

        # scrollbar
        scrollbar = tk.Scrollbar(self.file_frame)
        scrollbar.grid(row=1, column=3)

        self.tv.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tv.yview)

        self.inserer_fichiers_Bdd()

    def add(self, file: str) -> None:
        """
        Permets d'ajouter un élement à la liste (treeview)
        :param file: str, correspond à l'adresse d'un fichier
        :return:None
        """
        self.tout_select()
        items = self.tv.selection()
        if file != None:
            for newfile in file:
                for item in items:
                    data = list(self.tv.item(item).get("values"))
                    if newfile == data[1]:
                        return False
                self.tv.insert(parent='', index='end', values=("None", newfile, "None"))

    def suppr(self):
        """
        Permets de supprimer un élement de la liste
        :return: None
        """
        res = messagebox.askyesno('', 'Voulez-vous vraiment supprimer les fichers?')
        if res == True:
            for selected_item in self.tv.selection():
                self.tv.delete(selected_item)

    def tout_select(self) -> None:
        """
        Selectionne tout les élements de la liste
        :return:None
        """
        for item in self.tv.get_children():
            self.tv.selection_add(item)

    def visualisation(self) -> None:
        """
        Permets d'ouvrir la fenêtre pour visualiser le pdf et éditer le modèle
        :return: None
        """
        selected_item = self.tv.selection()[0]
        data = list(self.tv.item(selected_item).get("values"))
        v_fenetre = Visualisation_pdf(self.master, data[1], self.path, self.database, self.image_processor)
        v_fenetre.affichage()

    def open_fenetre_modèle(self) -> None:
        """
        Ouvre une fenêtre pour definir le modèle des élements selectionnés
        :return: None
        """
        self.fenetre_defmodele = Defenir_modele(self, self.path, self.database)
        self.fenetre_defmodele.affichage()

    def change_type_modele(self, type: str, modèle: str) -> None:
        """
        La fonction permets de definir le type et le modèle d'un element
        :param type: il s'agit d'un str du type du document facture ou fiche de paie
        :param modèle: str permets de definir le modèle d'un type
        :return: None
        """
        items = self.tv.selection()
        for selected_item in items:
            adresse = list(self.tv.item(selected_item).get("values"))[1]
            self.tv.item(item=selected_item, values=(type, adresse, modèle))

    def inserer_bdd(self) -> None:
        """
        Insertion des fichier et modèle dans la base de données
        :return:
        """
        items = self.tv.selection()
        liste_data = []
        for item in items:
            data = list(self.tv.item(item).get("values"))
            dict_données = {"fichier": data[1],
                            "modele": data[2]

                            }
            liste_data.append(dict_données)
        enregistrer(liste_data, self.database, self.image_processor, self.path)

    def inserer_fichiers_Bdd(self) -> None:
        """
        Cherche dans la BDD les PdF existant puis ajoute dans la liste
        :return:None
        """
        fichiers_Bdd = self.database.avoir_tous_les_fichiers()
        if fichiers_Bdd != None:
            for fichier in fichiers_Bdd:
                id = fichier.avoir_identifiant()
                modele = fichier.avoir_nom_modele()
                nom_fichier = fichier.avoir_nom_fichier()
                self.tv.insert(parent='', index='end', values=("None", nom_fichier, modele))


class Menu_p(tk.Frame):
    def __init__(self, master: tk.Frame, list_interface: Liste_interface_c):
        """
        Menu pour inserer un ou plusieurs fichiers
        :param master: Fenêtre avec qui le menu sera relié
        :param list_interface: liste de fichers de l'interface
        """
        super().__init__(master)
        self.master = master
        self.list = list_interface
        self.pack()

    def affichage(self) -> None:
        """
        Affichage du Menu deroulant en haut à gauche de l'interface
        :return: None
        """
        menu = Menu(master=self.master)
        element_menu = Menu(menu)
        element_menu.add_command(label='Ouvrir un fichier', command=self.Openfiles)
        menu.add_cascade(label="Menu", menu=element_menu)
        self.master.config(menu=menu)

    def Openfiles(self) -> None:
        """
        Permets d'ouvrir une fenêtre pour chercher un ou des fichers dans les dossiers de l'utilisateur puis l'ajouter dans la liste
        :return:
        """
        filenames = filedialog.askopenfilenames(initialdir="/", title="Select a File",
                                                filetypes=(("pdf", "*.pdf"), ("all files", "*.*")))
        self.list.add(filenames)
