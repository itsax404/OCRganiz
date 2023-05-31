from PIL import Image
import pytesseract
import fitz

class Image_Processor:

	def __init__(self, image, tesseract_dir: str):
		self.image = image
		self.tesseract_dir = tesseract_dir

	def crop(self, coordonnées: tuple[int]):
		image = Image.open(self.image)
		boite = tuple((coordonnées[0], coordonnées[1], coordonnées[2], coordonnées[3]))
		cropped_image = image.crop(boite)
		return cropped_image

	def ocr_cropped_image(self, image, lang="fra"):
		pytesseract.pytesseract.tesseract_cmd = self.tesseract_dir
		return pytesseract.image_to_string(image, lang=lang)
