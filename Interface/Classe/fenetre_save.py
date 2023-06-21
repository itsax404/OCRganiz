import json
import tkinter as tk
import os.path
from backend.classes.modele import Modele
from backend.database import Database


class Save_modele(tk.Toplevel):
    def __init__(self, type: str, main_path: str, database: Database):
        """
        Ouvre directement une fênetre avec le logo et dimension 200x200
        :param type: type de document facture/fiche de paie
        :param main_path: dossier racine du programme
        :param database: Base de données
        """
        super().__init__(master=None)
        self.title("Save modèle")
        self.geometry('275x200')
        self.database = database
        self.parent_dir = main_path
        self.type = type
        icon_path = os.path.join(self.parent_dir, "lib", 'icon.ico')
        self.iconbitmap(icon_path)
        self.list_rect = []

    def affichage(self) -> None:
        """
        Affiche toute la partie graphique
        :return:None
        """
        self.affichage_label()
        self.affichage_btn()

    def affichage_label(self) -> None:
        """
        Affichage du texte et de la zone de texte
        :return: None
        """
        label_frame = tk.Frame(master=self)
        label_frame.grid(row=0, column=0)

        label_text = tk.Label(master=label_frame, text="Voulez-vous vraiment enregistrer ?")
        label_text.grid(row=0, column=2, padx=10, pady=10)

        self.nom_modele = tk.Text(master=label_frame, height=1, width=20)
        self.nom_modele.grid(row=1, column=2, padx=10, pady=10)

    def affichage_btn(self) -> None:
        """
        Affichage des boutons pour annuler et sauvegarder
        :return: None
        """
        btn_frame = tk.Frame(master=self)
        btn_frame.grid(row=1, column=0)

        btn_annuler = tk.Button(master=btn_frame, text="Annuler", command=self.annuler)
        btn_annuler.grid(row=0, column=1, padx=10, pady=10)

        btn_save = tk.Button(master=btn_frame, text="Enregistrer", command=self.save)
        btn_save.grid(row=0, column=3, padx=10, pady=10)

        btn_export = tk.Button(master=btn_frame, text="Export modèle", command=self.exporter)
        btn_export.grid(row=1, column=2, padx=10, pady=10)

    def annuler(self) -> None:
        """
        Annule la sauvegarde du modèle
        :return:None
        """
        self.destroy()

    def set_data_rect(self, list_rect) -> None:
        """
        permet de recuperer une liste de réctangles
        :param list_rect: list de Detection_rect
        :return: None
        """
        self.list_rect = list_rect

    def save(self) -> None:
        """
        sauvegarde du modèle
        :return: None
        """
        self.ajouter_bdd()
        self.destroy()

    def creation_data_rect(self) -> None:
        """
        Permet la création d'une liste de coordonnées sous la forme de:
        [{"nom_modele": nom_modele, "type": self.type},
        {   "coordonnées":  rect.dimension(),
            "type": id.exemple1,
            "page": numero_page
                  }

        ]
        :return: None
        """
        input_text = self.nom_modele.get("1.0", "end-1c")
        nom_modele = input_text
        data_rect = [{"nom_modele": nom_modele, "type": self.type}]
        for rect in self.list_rect:
            dict = {"coordonnées": rect.dimension(),
                    "type": rect.get_id(),
                    "page": rect.get_nimg()
                    }
            data_rect.append(dict)

        return data_rect

    def ajouter_bdd(self) -> None:
        """
        Fonction pour ajouter un modèle dans la BDD
        :return: None
        """
        data_rect = self.creation_data_rect()
        modele = Modele(data_rect)
        self.database.ajouter_modele(modele)

    def exporter(self) -> None:
        """
        Permet d'exporter les coordonnées dans un fichier .modele
        :return: None
        """
        input_text = self.nom_modele.get("1.0", "end-1c")
        nom_modele = input_text
        data_rect = self.creation_data_rect()
        path = os.path.join(self.parent_dir, "modeles", f"{nom_modele}.modele")
        fichier = open(path, "w", encoding="UTF-8")
        fichier.write(json.dumps(data_rect, indent=4))
        fichier.close()
        self.destroy()
