import os
from backend.database import Database
from backend.images.image_processor import Image_Processor
from Interface.Interface import Interface
from backend.files.importeur_modele import Importateur

import dotenv


dotenv.load_dotenv()

TESSERACT_DIR = os.getenv("TESSERACT_DIR")

main_path = os.getcwd()

database = Database()
importeur = Importateur(main_path, database)
image_processor = Image_Processor(TESSERACT_DIR)
main_interface = Interface(main_path, database, image_processor)