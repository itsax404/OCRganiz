from images.image_processor import Image_Processor
import os


parent_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

ip = Image_Processor(os.path.join(parent_directory, "back-end", "images", "test", "image.jpg"), "C:\\Program Files\\Tesseract-OCR\\tesseract.exe")

image_cropped = ip.crop([(662, 362), (907, 415)])
image_cropped.show()
print(ip.ocr_cropped_image(image_cropped))
