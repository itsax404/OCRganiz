import datetime

from PIL import Image
import pytesseract

from backend.classes import Facture
from backend.classes.bases import Personne
from backend.classes.bases.adresse import Adresse
from backend.classes.bases.entreprise import Entreprise

from backend.images.reconnaisseurs.adresse_reconnaisseur import Adresse_Reconnaisseur
from backend.images.reconnaisseurs.entreprise_reconnaisseur import Entreprise_Reconnaisseur
from backend.images.reconnaisseurs.personne_reconnaisseur import Personne_Reconnaisseur
import os


class Image_Processor:
	"""
	TODO docstring car la classe est en construction
	"""

	def __init__(self, tesseract_dir: str):
		self.tesseract_dir = tesseract_dir
		self.adresse_reconnaisseur = Adresse_Reconnaisseur()
		self.entreprise_reconnaisseur = Entreprise_Reconnaisseur()
		self.personne_reconnaisseur = Personne_Reconnaisseur()

	def crop(self, image, coordonnées: tuple[int, int, int, int], path) -> Image:
		self.image = os.path.join(path, "output", "output_temp.jpg")
		image.save(self.image)
		image_pillow = Image.open(self.image)
		return image_pillow.crop(coordonnées)

	def __ocr_cropped_image__(self, image: Image, lang: str = "fra") -> str:
		pytesseract.pytesseract.tesseract_cmd = self.tesseract_dir
		return pytesseract.image_to_string(image, lang=lang)

	def __crop_and_ocr__(self, coordonnées: tuple[int, int, int, int], path, lang: str = "fra") -> str:
		cropped_image = self.crop(self.image, coordonnées, path)
		return self.__ocr_cropped_image__(cropped_image, lang=lang)

	def reconnaitre(self, images, coordonnees, type, path):
		"""
		coordonnee : [{"coordonnées": (int, int, int, int), "type": "*.*" , "page": int}]
		adresse : 'adresse'
			numéro de rue : 'adresse.numero'
			rue : 'adresse.rue'
			complement : 'adresse.complement'
			boite postale : 'adresse.boite_postale'
			code postal : 'adresse.code_postal'
			ville : 'adresse.ville'
			pays : 'adresse.pays'
		personne : 'personne'
			prenom : 'personne.prenom'
			nom : 'personne.nom'
		entreprise: 'entreprise'
			nom : 'entreprise.nom'
			adresse : 'entreprise.adresse'
		"""
		if type == "facture":
			acheteur = Personne()
			adresse = Adresse()
			enseigne = Entreprise(adresse=Adresse())
			prix_ht = 0.0
			prix_ttc = 0.0
			date_achat = None
			for coordonnee in coordonnees:
				page = coordonnee["page"]
				self.image = images[page-1]
				sous_parties = [partie for partie in coordonnee["type"].split(".") if partie != ""]
				coords = coordonnee["coordonnées"]
				ocr = self.__crop_and_ocr__(coords, path)
				print(f"{sous_parties} | ocr : {ocr}")
				if len(sous_parties) == 1:
					return None
				if sous_parties[0] == "adresse":
					match sous_parties[1]:
						case "numero":
							adresse.modifier_numero(ocr)
						case "rue":
							adresse.modifier_rue(ocr)
						case "complement":
							adresse.modifier_complement(ocr)
						case "boite_postale":
							adresse.modifier_boite_postale(ocr)
						case "code postal":
							adresse.modifier_code_postal(ocr)
						case "ville":
							adresse.modifier_ville(ocr)
						case "pays":
							adresse.modifier_pays(ocr)
				elif sous_parties[0] == "personne":
					match sous_parties[1]:
						case "nom":
							acheteur.modifier_nom(ocr)
						case "prenom":
							acheteur.modifier_prenom(ocr)

				elif sous_parties[0] == "entreprise":
					if len(sous_parties) == 3:
						if sous_parties[1] == "adresse":
							match sous_parties[2]:
								case "numero":
									enseigne.avoir_adresse().modifier_numero(ocr)
								case "rue":
									enseigne.avoir_adresse().modifier_rue(ocr)
								case "complement":
									enseigne.avoir_adresse().modifier_complement(ocr)
								case "boite_postale":
									enseigne.avoir_adresse().modifier_boite_postale(ocr)
								case "code postal":
									enseigne.avoir_adresse().modifier_code_postal(ocr)
								case "ville":
									enseigne.avoir_adresse().modifier_ville(ocr)
								case "pays":
									enseigne.avoir_adresse().modifier_pays(ocr)
					if len(sous_parties) == 2:
						if sous_parties[1] == "nom":
							enseigne.modifier_nom(ocr)
				elif sous_parties[0] == "date_achat":
					date_achat = (ocr)

				elif sous_parties[0] == "prix_ht" or sous_parties[0] == "prix_ttc":
					if sous_parties[0] == "prix_ht":
						prix_ht = float(ocr)
					else:
						prix_ttc = float(ocr)
				else:
					raise ValueError("Erreur")

				a = os.path.join(path, "output", "output_temp.jpg")
				if os.path.isfile(a):
					os.remove(a)
			print(enseigne)
			return Facture(acheteur, adresse, enseigne, prix_ht, prix_ttc, date_achat)
