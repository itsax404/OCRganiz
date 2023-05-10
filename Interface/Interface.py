import tkinter as tk
from tkinter import Menu, filedialog

#from Interface.Classe.Liste_interface import Liste_interface, affichagetest


def Openfile():
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("pdf", "*.pdf"), ("all files","*.*")))
    #list_file.append(filename)
    check.config(text="list_file[0]")
def Openfiles():
    filenames = filedialog.askopenfilenames(initialdir="/", title="Select a File", filetypes=(("pdf", "*.pdf"), ("all files","*.*")))
    check.configure(text="")
#
root = tk
onglet = root.Tk()

#
#
# Onglet principale
onglet.geometry("600x600")
onglet.title("Titre application")

#
menu = Menu(onglet)
element_menu = Menu(menu)
element_menu.add_command(label='Ouvrir fichier', command=Openfile)
element_menu.add_command(label='Ouvrir dossier', command=Openfiles)
menu.add_cascade(label="Menu", menu=element_menu)
onglet.config(menu=menu)


#root.Tk().iconbitmap('C:\Users\thoma\OneDrive\Documents\icone.jfif')
content = root.Frame(width=3000, height=1000)
content.grid(column=0, row=0)
content.pack(fill=root.X)
frame = root.Frame(master=content, borderwidth=5, relief="ridge")
frame.pack(fill=root.X)

file_frame = root.LabelFrame(frame, text="liste des fichiers")
file_frame.grid(row=0, column=0, padx=20, pady=20, sticky="news")
file_frame.pack(fill=root.X)

check_all = root.Checkbutton(master=file_frame, text="Selectionner tout les fichiers")
check_all.grid(row=0,column=0)

#list_file = Liste_interface(onglet)
#list_file.affichage()


label_a = root.Label(master=file_frame, text="Le nom du fichier")
label_a.grid(row=1, column=2)
check = root.Checkbutton(master=file_frame,text="numero 1")
check.grid(row=1, column=0)

check_1 = root.Checkbutton(master=file_frame, text="numero 2")
check_1.grid(row=2, column=0)

check.bind("<Enter>")
content.pack()


# start the program
root.mainloop()
