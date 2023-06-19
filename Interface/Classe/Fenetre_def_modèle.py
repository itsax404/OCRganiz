import tkinter as tk
import os.path
class Defenir_modele(tk.Toplevel):
    def __init__(self, list, main_path, database):
        super().__init__(master=None)
        self.title("Modèle")
        self.geometry('200x200')
        self.parent_dir = main_path
        self.database = database
        icon_path = os.path.join(self.parent_dir, "lib", 'icon.ico')
        self.iconbitmap(icon_path)
        self.list = list


    def affichage(self):

        self.affichage_label()
        self.affichage_choix()
        self.affichage_btn()


    def affichage_label(self):
        label_frame = tk.Frame(master=self)
        label_frame.grid(row=0, column=0)

        label_text_1 = tk.Label(master=label_frame, text="Definir un modèle et un type:")
        label_text_1.grid(row=0, column=0, padx=10, pady=10)

        #label_text_2 = tk.Label(master=label_frame, text="Le fichier pdf peut être soit une facture ou une fichie de paie, "
                                                         #"le modéle est defini par l'ulisateur par l'onglet 'Visualiser pdf'")
        #label_text_2.grid(row=1, column=2, padx=10, pady=10)


    def affichage_btn(self):
        btn_frame = tk.Frame(master=self)
        btn_frame.grid(row=2, column=0)

        btn_annuler = tk.Button(master=btn_frame, text="Annuler", command=self.annuler)
        btn_annuler.grid(row=0, column=1, padx=10, pady=10)

        btn_save = tk.Button(master=btn_frame, text="Enregistrer", command=self.enregister_modele)
        btn_save.grid(row=0, column=3, padx=10, pady=10)


    def affichage_choix(self):
        self.choix_frame = tk.Frame(master=self)
        self.choix_frame.grid(row=1, column=0)

        self.choix_type = tk.StringVar()
        self.str_choix = ("Facture", "Fiche de paie")
        self.choix_type.set(self.str_choix[0])

        self.option_type = tk.OptionMenu(self.choix_frame, self.choix_type, *self.str_choix, command=self.changmt_option)
        self.option_type.grid(row=0, column=0, padx=10)

        self.choix_modèle = tk.StringVar()
        self.str_modele = ("None","None")
        self.choix_modèle.set(self.str_choix[0])

        self.option_modele = tk.OptionMenu(self.choix_frame, self.choix_modèle, *self.str_modele)
        self.option_modele.grid(row=1, column=0, padx=10)


    def annuler(self):
        self.destroy()


    def changmt_option(self, event):
        newmodele = self.choix_type.get()
        list_modeles = self.database.avoir_tous_les_modeles()
        lignes = [modele.avoir_nom() for modele in list_modeles]
        print(lignes)
        if len(lignes) == 0:
            lignes = ["Aucun modèle"]
        self.str_modele = lignes
        self.update_option_modele()


    def update_option_modele(self):
        self.option_modele.destroy()
        self.choix_modèle = tk.StringVar()
        self.choix_modèle.set(self.str_choix[0])

        self.option_modele = tk.OptionMenu(self.choix_frame, self.choix_modèle, *self.str_modele)
        self.option_modele.grid(row=1, column=0, padx=10)


    def enregister_modele(self):
        self.list.change_type_modele()