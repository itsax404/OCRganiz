from PIL import Image
import pytesseract


class Image_Processor:

	"""
	TODO docstring car la classe est en construction
	"""

	def __init__(self, image, tesseract_dir: str):
		self.image = image
		self.tesseract_dir = tesseract_dir

	def crop(self, coordonnées: tuple[int, int, int, int]) -> Image:
		image = Image.open(self.image)
		return image.crop(coordonnées)

	def __ocr_cropped_image__(self, image: Image, lang: str = "fra") -> str:
		pytesseract.pytesseract.tesseract_cmd = self.tesseract_dir
		return pytesseract.image_to_string(image, lang=lang)

	def __crop_and_ocr__(self, coordonnées: tuple[int, int, int, int], lang: str = "fra") -> str:
		cropped_image = self.crop(coordonnées)
		return self.__ocr_cropped_image__(cropped_image, lang=lang)

	def detecte_adresse(self, coordonnées: tuple[int, int, int, int], lang: str = "fra") -> str:
		texte_adresse = self.__crop_and_ocr__(coordonnées, lang=lang)
		f = open(".\\text.txt", "w")
		f.write(texte_adresse)
		f.close()
		print(texte_adresse)
