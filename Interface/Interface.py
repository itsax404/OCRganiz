import tkinter as tk
import os.path
from backend.database import Database
from backend.images.image_processor import Image_Processor
from Interface.Classe.Liste_interface import Liste_interface_c, Menu_p


class Interface:
    def __init__(self, main_path: str, database: Database, image_processor: Image_Processor):

        """
        Initialisation de l'interface principale
        :param main_path: dossier racine du programme
        :param database: Base de données
        :param image_processor: objet qui gère le img et OCR
        """
        self.master = tk.Tk()
        self.database = database
        self.image_processor = image_processor
        self.master.title("OCRganiz")
        self.master.geometry('800x800')
        self.main_path = main_path
        icon_path = os.path.join(self.main_path, "lib", 'icon.ico')
        self.master.iconbitmap(icon_path)

        self.affichage()
        self.master.mainloop()
        self.delete_output()

    def affichage(self) -> None:
        """
        Affichage de l'interface principale
        :return: None
        """
        list_file = Liste_interface_c(self.master, self.main_path, self.database, self.image_processor)
        menu = Menu_p(self.master, list_interface=list_file)

        menu.affichage()
        list_file.affichage()

    def delete_output(self) -> None:
        """
        suppprime toute les img .png du dossier 'output
        :return:
        """
        dir = os.path.join(self.main_path, "output")
        for img in os.scandir(dir):
            extension = os.path.splitext(img.path)[1]
            if extension == ".png":
                os.remove(img.path)
