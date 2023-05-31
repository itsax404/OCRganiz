import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import fitz
from backend.images.image_processor import Image_Processor


class visualisation_pdf(tk.Toplevel):
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
        self.img = self.img.resize((int(self.WIDTH * 0.22), int(self.HEIGHT * 0.22)))
        self.img = ImageTk.PhotoImage(self.img)
        self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
        self.rect_id = None

        self.affichage()

    def affichage(self):
        labelframe = tk.LabelFrame(master=self, text="liste des fichiers")
        labelframe.pack(side="left", fill=tk.Y, padx=10)

        label = tk.Label(labelframe, text="")
        label.grid(row=0, column=0)
        btn = tk.Button(labelframe, text="test", command=self.test)
        btn.grid()
        frame = tk.Frame(master=self, width=self.w, height=self.h)
        frame.pack(side="left", fill=tk.Y, padx=10)

        self.canvas = tk.Canvas(master=frame, width=self.WIDTH * 0.22, height=self.HEIGHT * 0.22,
                                borderwidth=0, highlightthickness=0, scrollregion=(0, 0, 500, 500))

        self.canvas.img = self.img
        self.canvas.create_image(0, 0, image=self.img, anchor=tk.NW)

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
        ip = Image_Processor("C:\\Users\\thoma\\PycharmProjects\\projet-programmation\\test\\output0.png", "C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
        image_cropped = ip.crop(tuple((self.topx * 4.54, self.topy * 4.54, self.botx * 4.54, self.boty * 4.54)))
        height, weight = image_cropped.size
        if not (height == 0 or weight == 0):
            print(ip.ocr_cropped_image(image_cropped))

    def get_mouse_posn(self, event):
        self.topx, self.topy = event.x, event.y

    def update_sel_rect(self, event):
        self.botx, self.boty = event.x, event.y
        print(self.topx, self.topy, self.botx, self.boty)
        self.canvas.coords(self.rect_id, self.topx, self.topy, self.botx, self.boty)