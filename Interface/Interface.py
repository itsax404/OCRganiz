import tkinter as tk
from tkinter import Menu, filedialog

from Classe.Liste_interface import Liste_interface

def Openfiles():
    filenames = filedialog.askopenfilenames(initialdir="/", title="Select a File", filetypes=(("pdf", "*.pdf"), ("all files","*.*")))
    list_file.add(filenames)
#
root = tk
onglet = root.Tk()

#
#
# Onglet principale
onglet.geometry("800x800")
onglet.title("Titre application")
#
menu = Menu(onglet)
element_menu = Menu(menu)
element_menu.add_command(label='Ouvrir fichier', command=Openfiles)
menu.add_cascade(label="Menu", menu=element_menu)
onglet.config(menu=menu)


#root.Tk().iconbitmap('C:\Users\thoma\OneDrive\Documents\icone.jfif')

list_file = Liste_interface(onglet)
list_file.affichage()



# start the program
root.mainloop()