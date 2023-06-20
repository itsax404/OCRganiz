import tkinter as tk
import os.path
from Interface.Classe.Liste_interface import Liste_interface_c, Menu_p


class Interface:
    def __init__(self, main_path, database, image_processor):
        self.master = tk.Tk()
        self.database = database
        self.image_processor = image_processor
        self.master.title("Titre application")
        self.master.geometry('800x800')
        self.main_path = main_path
        icon_path = os.path.join(self.main_path, "lib", 'icon.ico')
        self.master.iconbitmap(icon_path)

        self.affichage()
        self.master.mainloop()
        self.delete_output()

    def affichage(self):
        list_file = Liste_interface_c(self.master, self.main_path, self.database, self.image_processor)
        menu = Menu_p(self.master, list_interface=list_file)

        menu.affichage()
        list_file.affichage()

    def delete_output(self):
        # suppression des img
        dir = os.path.join(self.main_path, "output")
        for img in os.scandir(dir):
            extension = os.path.splitext(img.path)[1]
            if extension == ".png":
                os.remove(img.path)
