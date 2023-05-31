import tkinter as tk
from Classe.Liste_interface import Liste_interface, Menu_p

#
root = tk
onglet = root.Tk()
#
#
# fênetre principale
onglet.geometry("800x800")
onglet.title("Titre application")
#root.Tk().iconbitmap('C:\Users\thoma\OneDrive\Documents\icone.jfif')
#

list_file = Liste_interface(onglet)
menu = Menu_p(onglet, list_interface=list_file)

menu.affichage()
list_file.affichage()

# start the program
root.mainloop()