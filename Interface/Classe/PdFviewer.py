import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import fitz
from backend.images.image_processor import Image_Processor


class Visualisation_pdf(tk.Toplevel):
    def __init__(self, master, path):
        super().__init__(master=None)
        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.title("Visual pdf")
        self.geometry('%sx%s' % (self.w, self.h))
        self.path = path
        self.imgfiles = []
        self.pdfimg(self.path)

        self.img = Image.open(self.imgfiles[0])
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

        self.canvas = tk.Canvas(master=self.frame, width=self.WIDTH * 0.22, height=self.HEIGHT * 0.22,
                                borderwidth=0, highlightthickness=0, scrollregion=(0, 0, 500, 500))

        self.img = self.img.resize((int(self.WIDTH * 0.22), int(self.HEIGHT * 0.22)))
        self.img = ImageTk.PhotoImage(self.img)

        self.canvas.img = self.img
        self.canvas.create_image(0, 0, image=self.img, anchor=tk.NW)
        self.canvas.pack()

        btn_nextpage = tk.Button(self.frame, text="next", command=self.change_page)
        btn_nextpage.pack()

        self.rect_id = self.canvas.create_rectangle(self.topx, self.topy, self.topx, self.topy,
                                                    dash=(2, 2), fill='', outline='red')

        self.canvas.bind('<Button-1>', self.get_mouse_posn)
        self.canvas.bind('<B1-Motion>', self.update_sel_rect)

    def pdfimg(self, path):
        """
        Convertion des pdf en img .png
        :return:
        permet de enregistrer chaque page du pdf en .png
        """
        doc = fitz.open(path)
        pages = doc.pages()
        images = [page.get_pixmap(dpi=300) for page in pages]
        for img, i in zip(images, range(len(images))):
            img.save(f'C:\\Users\\thoma\\PycharmProjects\\projet-programmation\\test\\output{i}.png')
            self.imgfiles.append(f'C:\\Users\\thoma\\PycharmProjects\\projet-programmation\\test\\output{i}.png')

    def test(self):
        ip = Image_Processor("C:\\Users\\thoma\\PycharmProjects\\projet-programmation\\test\\output0.png",
                             "C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
        coordonnees = tuple((self.topx * 4.54, self.topy * 4.54, self.botx * 4.54, self.boty * 4.54))
        image_cropped = ip.crop(tuple((self.topx * 4.54, self.topy * 4.54, self.botx * 4.54, self.boty * 4.54)))
        height, weight = image_cropped.size
        if not (height == 0 or weight == 0):
            print(ip.__ocr_cropped_image__(image_cropped))

    def get_mouse_posn(self, event):
        self.topx, self.topy = event.x, event.y

    def update_sel_rect(self, event):
        self.botx, self.boty = event.x, event.y
        self.canvas.coords(self.rect_id, self.topx, self.topy, self.botx, self.boty)

    def change_page(self):
        self.img = Image.open(self.imgfiles[1])
        self.img = self.img.resize((int(self.WIDTH * 0.22), int(self.HEIGHT * 0.22)))
        self.canvas.itemconfig(self.frame, image=self.img)
        self.canvas.pack()
