import tkinter as tk
# create the application
root = tk

#
# here are method calls to the window manager class
#
root.Tk().geometry("2000x2000")
#root.Tk().iconbitmap('C:\Users\thoma\OneDrive\Documents\icone.jfif')
content = root.Frame(width=1000, height=1000)
frame_a = root.Frame(master=content, borderwidth=5, relief="ridge", width=150, height=150)


label_a = root.Label(master=frame_a, text="Le nom du fichier")
label_a.grid(row=0,column=1)
button = root.Checkbutton(master=frame_a, text="Quit")
button.grid(row=0,column=0)
button.bind("<Enter>")
content.pack()
frame_a.pack()

# start the program
root.mainloop()
