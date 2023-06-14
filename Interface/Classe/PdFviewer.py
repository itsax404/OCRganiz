import os.path
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import fitz
from backend.images.image_processor import Image_Processor
from .Zone_detection import Detection_rect
from .Tree_selection import List_selection_rect

class Visualisation_pdf(tk.Toplevel):
    def __init__(self, master, path, parent_dir):
        super().__init__(master=None)
        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.title("Visual pdf")
        self.geometry('%sx%s' % (self.w, self.h))
        self.path = path
        self.parent_dir = parent_dir
        self.imgfiles = []
        self.imgscale = 0.25
        self.canvasscale = 1
        self.pdfimg()
        self.n_img = 0

        self.posx = 0
        self.posy = 0

        self.newposx = 0
        self.newposy = 0

        self.translation_x = 0
        self.translation_y = 0

        self.list_detection_rect = []

        self.img = Image.open(self.imgfiles[self.n_img])
        self.WIDTH, self.HEIGHT = self.img.width, self.img.height

        self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
        self.rect_id = None

    def affichage(self):
        self.labelframe = tk.LabelFrame(master=self, text="liste des fichiers")
        self.labelframe.pack(side="left", fill=tk.Y, padx=10)

        self.label = tk.Label(self.labelframe, text="")
        self.label.grid(row=0, column=0, padx=10)

        btn = tk.Button(self.labelframe, text="test", command=self.test)
        btn.grid(row=0, column=0, padx=10)

        btn2 = tk.Button(self.labelframe, text="debug", command=self.debug)
        btn2.grid(row=0, column=1, padx=10)


        self.choix_modèle = tk.StringVar()
        self.str_choix = ("Facture", "Fiche de paie")
        self.choix_modèle.set(self.str_choix[0])

        self.option_menu = tk.OptionMenu(self.labelframe, self.choix_modèle, *self.str_choix, command=self.changmt_option)
        self.option_menu.grid(row=0, column=2)

        self.list_tree = List_selection_rect(self.labelframe, self.choix_modèle.get())
        self.list_tree.affichage()

        self.frame = tk.Frame(master=self, width=self.w, height=self.h)
        self.frame.pack(side="left", fill=tk.Y, padx=10)



        self.canvas = tk.Canvas(master=self.frame, width=self.WIDTH * self.imgscale, height=self.HEIGHT * self.imgscale,
                                borderwidth=0, highlightthickness=0, background="green")


        self.img = self.img.resize((int(self.WIDTH * self.imgscale), int(self.HEIGHT * self.imgscale)))
        self.img = ImageTk.PhotoImage(self.img)

        self.canvas.img = self.img


        self.img_canvas = self.canvas.create_image(0, 0, image=self.img, anchor=tk.NW)
        self.canvas.grid(row=0, column=1)


        btn_nextpage = tk.Button(self.frame, text=">", command=self.change_page)
        btn_nextpage.grid(row=0, column=2)


        btn_previouspage = tk.Button(self.frame, text="<", command=self.change_page)
        btn_previouspage.grid(row=0, column=0)

        self.text_nbpage = tk.Text(self.frame, height=2, width=2)
        self.text_nbpage.insert(tk.END, "0")
        self.text_nbpage.grid(row=1, column=1)

        self.rect_id = self.canvas.create_rectangle(self.topx, self.topy, self.topx, self.topy,
                                                    dash=(2, 2), fill='', outline='red')

        self.canvas.bind('<Button-3>', self.pos)
        self.canvas.bind('<B3-Motion>', self.new_pos)
        self.canvas.bind('<ButtonRelease-3>',  self.calcul_translation)

        self.canvas.bind('<Button-1>', self.get_mouse_posn)
        self.canvas.bind('<B1-Motion>', self.update_sel_rect)

        self.canvas.bind('<Button-2>', self.recentrage_image)
        self.canvas.bind("<MouseWheel>", self.zoom)

    def pdfimg(self):
        """
        Convertion des pdf en img .png
        :return:
        permet de enregistrer chaque page du pdf en .png
        """
        doc = fitz.open(self.path)
        pages = doc.pages()
        images = [page.get_pixmap(dpi=300) for page in pages]
        for img, i in zip(images, range(len(images))):
            output_path = os.path.join(self.parent_dir, "test", f"output {i}.png")
            img.save(output_path)
            self.imgfiles.append(output_path)

    def test(self):
        self.list_detection_rect.append(Detection_rect(self.imgscale, self.topx, self.topy, self.botx, self.boty, self.translation_x, self.translation_y, self.n_img))
        n=self.list_detection_rect[0].get_nimg()
        output_path = os.path.join(self.imgfiles[n])
        ip = Image_Processor(output_path,
                             "C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
        image_cropped = ip.crop(coordonnées=self.list_detection_rect[0].dimension())
        height, weight = image_cropped.size
        if not (height == 0 or weight == 0):
            ip.detecte_adresse(coordonnées=self.list_detection_rect[0].dimension())

    def get_mouse_posn(self, event):
        self.topx, self.topy = event.x, event.y


    def update_sel_rect(self, event):
        self.botx, self.boty = event.x, event.y
        self.canvas.coords(self.rect_id, self.topx - self.translation_x, self.topy - self.translation_y, self.botx - self.translation_x, self.boty - self.translation_y )

    def change_page(self):
        self.n_img += 1
        if self.n_img == len(self.imgfiles):
            self.n_img = 0

        self.update_image()
        self.text_nbpage.delete("1.0", "end-1c")
        self.text_nbpage.insert(tk.END, self.n_img)

    def zoom(self, event):
        delta = 0.75
        self.canvasscale = 1
        if event.num == 5 or event.delta == -120:
            self.imgscale *= delta

        if event.num == 4 or event.delta == 120:
            self.imgscale /= delta
        print(self.posx, self.posy, self.canvasscale)
        self.update_image()

    def update_image(self):
        self.img = Image.open(self.imgfiles[self.n_img])
        self.img = self.img.resize((int(self.WIDTH * self.imgscale), int(self.HEIGHT * self.imgscale)))
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.img_canvas, image=self.img)
        self.canvas.lower(self.img_canvas)
        self.canvas.grid(row=0, column=1)


    def recentrage_image(self, event):
        self.canvasscale = 1
        self.posx = 0
        self.posy = 0
        self.newposx = 0
        self.newposy = 0
        self.translation_x = 0
        self.translation_y = 0
        self.imgscale = 0.25
        self.canvas.delete(self.img_canvas)
        self.img_canvas = None
        self.canvas.imagetk = None
        self.canvas.scale('all', self.posx, self.posy, self.canvasscale, self.canvasscale)
        self.canvas.grid()
        self.img_canvas = self.canvas.create_image(0, 0, image=self.img, anchor=tk.NW)
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        self.update_image()

    def debug(self):
        for rect in self.list_detection_rect:
            self.canvas.coords(self.rect_id, rect.get_topx(), rect.get_topy(), rect.get_botx(), rect.get_boty())


    def new_pos(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.newposx = event.x
        self.newposy = event.y
        self.newposx = self.newposx - self.posx
        self.newposy = self.newposy - self.posy


    def pos(self, event):
        self.canvas.scan_mark(event.x, event.y)
        self.posx = event.x
        self.posy = event.y


    def calcul_translation (self, event):
        self.translation_x += self.newposx
        self.translation_y += self.newposy


    def changmt_option (self, event):
        newmodele = self.choix_modèle.get()
        self.list_tree.set_modele(newmodele)
        self.list_tree.update_tree()
        self.list_tree.ajouter_enfant("thomas")