import tkinter as tk
from Classe.Liste_interface import Liste_interface_c, Menu_p

#
root = tk
onglet = root.Tk()
#
#
# fênetre principale
onglet.geometry("800x800")
onglet.title("Titre application")
onglet.iconbitmap('C:\\Users\\thoma\\PycharmProjects\\projet-programmation\\lib\\icon.ico')
#

list_file = Liste_interface_c(onglet)
menu = Menu_p(onglet, list_interface=list_file)

menu.affichage()
list_file.affichage()

# start the program
root.mainloop()