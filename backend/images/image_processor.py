from PIL import Image
import pytesseract


class Image_Processor:

	def __init__(self, image, tesseract_dir: str):
		self.image = image
		self.tesseract_dir = tesseract_dir

	def crop(self, coordonnées: tuple[int, int, int, int]) -> Image:
		image = Image.open(self.image)
		return image.crop(coordonnées)

	def ocr_cropped_image(self, image: Image, lang: str = "fra") -> str:
		pytesseract.pytesseract.tesseract_cmd = self.tesseract_dir
		return pytesseract.image_to_string(image, lang=lang)

	def crop_and_ocr(self, coordonnées: tuple[int, int, int, int], lang: str = "fra") -> str:
		cropped_image = self.crop(coordonnées)
		return self.ocr_cropped_image(cropped_image, lang=lang)
