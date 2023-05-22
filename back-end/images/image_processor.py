from PIL import Image
import pytesseract


class Image_Processor:

	def __init__(self, image, tesseract_dir: str):
		self.image = image
		self.tesseract_dir = tesseract_dir

	def crop(self, coordonnées: list[tuple[int]]):
		image = Image.open(self.image)
		boite = tuple((coordonnées[0][0], coordonnées[0][1], coordonnées[1][0], coordonnées[1][1]))
		cropped_image = image.crop(boite)
		return cropped_image

	def ocr_cropped_image(self, image, lang="fra"):
		pytesseract.pytesseract.tesseract_cmd = self.tesseract_dir
		return pytesseract.image_to_string(image, lang=lang)
