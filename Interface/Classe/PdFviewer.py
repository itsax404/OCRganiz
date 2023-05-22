import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import fitz



def get_mouse_pos(event):
    global topy, topx

    topx, topy = event.x, event.y

def update_sel_rect(event):
    global rect_id
    global topy, topx, botx, boty

    botx, boty = event.x, event.y
    print(topx, topy, botx, boty)
    canvas.coords(rect_id, topx, topy, botx, boty)  # Update selection rect.


def pdfimg():
#    try:
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "factureEdF.pdf")
# "        C:\Users\thoma\PycharmProjects\projet - programmation\test\factureEdF.pdf"
    print(path)
    doc = fitz.open(path)
    pages = doc.pages()
    images = [page.get_pixmap(dpi=300) for page in pages]
    for img, i in zip(images, range(len(images))):
        img.save(f'output{i}.png')

#    except:
#        Result = "NO pdf found"
#        messagebox.showinfo("Result", Result)

#    else:
#        Result = "success"
#        messagebox.showinfo("Result", Result)


path = "test\\output0.png"
img = Image.open(path)
#pdfimg()
WIDTH, HEIGHT = img.width, img.height
topx, topy, botx, boty = 0, 0, 0, 0
rect_id = None

window = tk.Tk()
window.title("Select Area")
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry('%sx%s' % (w, h))
window.configure(background='grey')

img = img.resize((int(WIDTH*0.2), int(HEIGHT*0.2)))
img = ImageTk.PhotoImage(img)

#img = ImageTk.PhotoImage(img)
frame = tk.Frame(window, width=w, height=h)
frame.grid(row=0, column=0)
canvas = tk.Canvas(master=frame, width=WIDTH*0.2, height=HEIGHT*0.2,
                   borderwidth=0, highlightthickness=0, scrollregion=(0, 0, 500, 500))

canvas.img = img  # Keep reference in case this code is put into a function.
canvas.create_image(0, 0, image=img, anchor=tk.NW)
scrollbar = tk.Scrollbar(master=frame)
scrollbar.grid(row=0, column=2)
canvas.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=canvas.yview)
canvas.grid(row=0, column=1)
# Create selection rectangle (invisible since corner points are equal).
rect_id = canvas.create_rectangle(topx, topy, topx, topy,
                                  dash=(2,2), fill='', outline='red')

canvas.bind('<Button-1>', get_mouse_pos)
canvas.bind('<B1-Motion>', update_sel_rect)

window.mainloop()