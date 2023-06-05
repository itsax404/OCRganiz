import os.path
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import fitz
from backend.images.image_processor import Image_Processor


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
        self.pdfimg()
        self.n_img = 0

        self.img = Image.open(self.imgfiles[self.n_img])
        self.WIDTH, self.HEIGHT = self.img.width, self.img.height

        self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
        self.rect_id = None

    def affichage(self):
        self.labelframe = tk.LabelFrame(master=self, text="liste des fichiers")
        self.labelframe.pack(side="left", fill=tk.Y, padx=10)

        self.label = tk.Label(self.labelframe, text="")
        self.label.grid(row=0, column=0)
        btn = tk.Button(self.labelframe, text="test", command=self.test)
        btn.grid()

        self.frame = tk.Frame(master=self, width=self.w, height=self.h)
        self.frame.pack(side="left", fill=tk.Y, padx=10)



        self.canvas = tk.Canvas(master=self.frame, width=self.WIDTH * self.imgscale, height=self.HEIGHT * self.imgscale,
                                borderwidth=0, highlightthickness=0, scrollregion=(0, 0, 500, 500), background="green")

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
        self.text_nbpage.insert(tk.END, "1")
        self.text_nbpage.grid(row=1, column=1)

        self.rect_id = self.canvas.create_rectangle(self.topx, self.topy, self.topx, self.topy,
                                                    dash=(2, 2), fill='', outline='red')

        self.canvas.bind('<Button-1>', self.get_mouse_posn)
        self.canvas.bind('<B1-Motion>', self.update_sel_rect)
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
            output_path = os.path.join(self.parent_dir, "test", f"output{i}.png")
            img.save(output_path)
            self.imgfiles.append(output_path)

    def test(self):
        output_path = os.path.join(self.parent_dir, "test", f"output0.png")
        ip = Image_Processor(output_path,
                             "C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
        coordonnees = tuple((self.topx * 4.54, self.topy * 4.54, self.botx * 4.54, self.boty * 4.54))
        image_cropped = ip.crop(tuple((self.topx * (1/self.imgscale), self.topy * (1/self.imgscale), self.botx * (1/self.imgscale), self.boty * (1/self.imgscale))))
        height, weight = image_cropped.size
        if not (height == 0 or weight == 0):
            print(ip.__ocr_cropped_image__(image_cropped))

    def get_mouse_posn(self, event):
        self.topx, self.topy = event.x, event.y

    def update_sel_rect(self, event):
        self.botx, self.boty = event.x, event.y
        self.canvas.coords(self.rect_id, self.topx, self.topy, self.botx, self.boty)

    def change_page(self):
        self.n_img += 1
        if self.n_img == len(self.imgfiles):
            self.n_img = 0

        self.update_image()
        self.text_nbpage.delete("1.0", "end-1c")
        self.text_nbpage.insert(tk.END, self.n_img)

    def zoom(self, event):
        delta = 0.75
        scale = 1
        if event.num == 5 or event.delta == -120:
            self.imgscale *= delta
            scale *= delta
        if event.num == 4 or event.delta == 120:
            self.imgscale /= delta
            scale /= delta
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale('all', x, y, scale, scale)
        self.update_image()

    def update_image(self):
        self.img = Image.open(self.imgfiles[self.n_img])
        self.img = self.img.resize((int(self.WIDTH * self.imgscale), int(self.HEIGHT * self.imgscale)))
        self.img = ImageTk.PhotoImage(self.img)
        self.canvas.itemconfig(self.img_canvas, image=self.img)
        self.canvas.grid(row=0, column=1)
