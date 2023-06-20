import tkinter as tk
import os.path


class Defenir_modele(tk.Toplevel):
    def __init__(self, list: str, main_path: str, database):
        """
        :param list: str[] list des fichiers selectionnés
        :param main_path: str dossier racine du programme
        :param database:
        """
        super().__init__(master=None)
        self.title("Modèle")
        self.geometry('200x200')
        self.parent_dir = main_path
        self.database = database
        icon_path = os.path.join(self.parent_dir, "lib", 'icon.ico')
        self.iconbitmap(icon_path)
        self.list = list

    def affichage(self):
        """
        Affiche l'interface graphique
        :return: None
        """
        self.affichage_label()
        self.affichage_choix()
        self.affichage_btn()

    def affichage_label(self):
        """
        Affichage du texte
        :return: None
        """
        label_frame = tk.Frame(master=self)
        label_frame.grid(row=0, column=0)

        label_text_1 = tk.Label(master=label_frame, text="Definir un modèle et un type:")
        label_text_1.grid(row=0, column=0, padx=10, pady=10)

    def affichage_btn(self):
        """
        Affichage des boutons 'Annuler' et 'Enrigistrer'
        :return: None
        """
        btn_frame = tk.Frame(master=self)
        btn_frame.grid(row=2, column=0)

        btn_annuler = tk.Button(master=btn_frame, text="Annuler", command=self.annuler)
        btn_annuler.grid(row=0, column=1, padx=10, pady=10)

        btn_save = tk.Button(master=btn_frame, text="Enregistrer", command=self.enregister_modele)
        btn_save.grid(row=0, column=3, padx=10, pady=10)

    def affichage_choix(self):
        """
        Affichage des options deroulant pour choisir un type et un modèle
        :return: None
        """
        self.choix_frame = tk.Frame(master=self)
        self.choix_frame.grid(row=1, column=0)

        self.choix_type = tk.StringVar()
        self.str_choix = ("Facture", "Fiche de paie")
        self.choix_type.set(self.str_choix[0])

        self.option_type = tk.OptionMenu(self.choix_frame, self.choix_type, *self.str_choix,
                                         command=self.changmt_option)
        self.option_type.grid(row=0, column=0, padx=10)

        self.choix_modèle = tk.StringVar()
        self.str_modele = ("None", "None")
        self.choix_modèle.set("None")

        self.option_modele = tk.OptionMenu(self.choix_frame, self.choix_modèle, *self.str_modele)
        self.option_modele.grid(row=1, column=0, padx=10)
        self.changmt_option(None)
        self.update_option_modele()

    def annuler(self):
        """
        Annuler le processus
        :return: None
        """
        self.destroy()

    def changmt_option(self, event=None):
        """
        Recuperation des modèles depuis la base de données et changement des options
        :param event: event du OptionMenu
        :return: None
        """
        list_modeles = self.database.avoir_tous_les_modeles()
        lignes = [modele.avoir_nom() for modele in list_modeles]
        print(lignes)
        if len(lignes) == 0:
            lignes = ["Aucun modèle"]
        self.str_modele = lignes
        self.update_option_modele()

    def update_option_modele(self):
        """
        Mise à jour des options deroulant qui gère les modèles
        :return: None
        """
        self.option_modele.destroy()

        self.choix_modèle = tk.StringVar()
        self.choix_modèle.set("None")

        self.option_modele = tk.OptionMenu(self.choix_frame, self.choix_modèle, *self.str_modele)
        self.option_modele.grid(row=1, column=0, padx=10)

    def enregister_modele(self):
        """
        Enregistre les fichers avec le type et modèle choisis
        :return: None
        """
        type = self.choix_type.get()
        modèle = self.choix_modèle.get()
        self.list.change_type_modele(type, modèle)
        self.destroy()
