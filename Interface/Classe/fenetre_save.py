import tkinter as tk
from .Zone_detection import Detection_rect
import os.path
from backend.classes.modele import Modele
class Save_modele(tk.Toplevel):
    def __init__(self,type, main_path, database):
        super().__init__(master=None)
        self.title("Visual pdf")
        self.geometry('200x200')
        self.database = database
        self.parent_dir = main_path
        self.type = type
        icon_path = os.path.join(self.parent_dir, "lib", 'icon.ico')
        self.iconbitmap(icon_path)
        self.list_rect=[]


    def affichage(self):
        self.affichage_label()
        self.affichage_btn()


    def affichage_label(self):
        label_frame = tk.Frame(master=self)
        label_frame.grid(row=0, column=0)

        label_text = tk.Label(master=label_frame, text="Voulez-vous vraiment enregister ?")
        label_text.grid(row=0, column=2, padx=10, pady=10)

        self.nom_modele = tk.Text(master=label_frame, height=1, width=20)
        self.nom_modele.grid(row=1, column=2, padx=10 , pady=10)


    def affichage_btn(self):
        btn_frame = tk.Frame(master=self)
        btn_frame.grid(row=1, column=0)

        btn_annuler = tk.Button(master=btn_frame, text="Annuler", command=self.annuler)
        btn_annuler.grid(row=0, column=1, padx=10, pady=10)

        btn_save = tk.Button(master=btn_frame, text="Enregistrer", command=self.save)
        btn_save.grid(row=0, column=3, padx=10, pady=10)


    def annuler(self):
        self.destroy()


    def set_data_rect(self, list_rect):
        self.list_rect = list_rect


    def save(self):
        self.creation_data_rect()


    def ajouter_modele(self, input_text):
        pass


    def creation_data_rect(self):
        input_text = self.nom_modele.get("1.0", "end-1c")
        nom_fichier = input_text
        data_rect = [{"nom_modele": nom_fichier, "type": self.type}]
        for rect in self.list_rect:
            dict={"coordonnées":  rect.dimension(),
                  "type": rect.get_id()
                  }
            data_rect.append(dict)
        modele = Modele(data_rect)
        self.database.ajouter_modele(modele)


    def extraction_data_rect(self, path):
        fichier = open(path, "r")
        lignes = fichier.readlines()
        fichier.close()

        data_rect = lignes[0]
        data_rect = eval(data_rect)
        print(data_rect[1]['type'])