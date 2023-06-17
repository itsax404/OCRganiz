import tkinter as tk
from .Zone_detection import Detection_rect
import os.path
class Save_modele(tk.Toplevel):
    def __init__(self):
        super().__init__(master=None)
        self.title("Visual pdf")
        self.geometry('200x200')
        self.parent_dir = os.path.join(os.path.realpath(__file__), os.pardir, os.pardir, os.pardir)
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
        input_text = self.nom_modele.get("1.0", "end-1c")
        self.ajouter_modele(input_text)
        nom_fichier = input_text + "_datarect"
        fichier_path = os.path.join(self.parent_dir, "Config_interface", 'Modèle', nom_fichier)
        print(fichier_path)
        self.creation_data_rect(fichier_path)

        #print(data_rect[('Acheteur', 'Acheteur.Prenom')])


    def ajouter_modele(self, input_text):
        fichier_path = os.path.join(self.parent_dir, "Config_interface", 'Modèle', 'Modèle_save')
        fichier_model = open(fichier_path, "w")
        fichier_model.write("\n" + input_text)
        fichier_model.close()


    def creation_data_rect(self, path):
        fichier_model = open(path, "w")
        data_rect = {}
        for rect in self.list_rect:
            data_rect[rect.get_id()] = rect.dimension()
        fichier_model.write(str(data_rect))
        fichier_model.close()