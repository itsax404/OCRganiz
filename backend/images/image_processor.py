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


class Image_Processor:
	"""
	TODO docstring car la classe est en construction
	"""

	def __init__(self, tesseract_dir: str):
		self.tesseract_dir = tesseract_dir
		self.adresse_reconnaisseur = Adresse_Reconnaisseur()
		self.entreprise_reconnaisseur = Entreprise_Reconnaisseur()
		self.personne_reconnaisseur = Personne_Reconnaisseur()

	def crop(self, image, coordonnées: tuple[int, int, int, int]) -> Image:
		self.image = image
		image_pillow = Image.open(self.image)
		return image_pillow.crop(coordonnées)

	def __ocr_cropped_image__(self, image: Image, lang: str = "fra") -> str:
		pytesseract.pytesseract.tesseract_cmd = self.tesseract_dir
		return pytesseract.image_to_string(image, lang=lang)

	def __crop_and_ocr__(self, coordonnées: tuple[int, int, int, int], lang: str = "fra") -> str:
		cropped_image = self.crop(self.image, coordonnées)
		return self.__ocr_cropped_image__(cropped_image, lang=lang)

	def reconnaitre(self, images, coordonnees, type):
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
			enseigne = Entreprise()
			prix_ht = 0.0
			prix_ttc = 0.0
			date_achat = None
			for coordonnee in coordonnees:
				page = coordonnee["page"]
				self.image = images[page-1]
				sous_parties = [partie for partie in coordonnee["type"].split(".") if partie != ""]
				coords = coordonnee["coordonnées"]
				if len(sous_parties) == 1:
					return None
				if sous_parties[0] == "adresse":
					match sous_parties[1]:
						case "numero":
							adresse.modifier_numero(self.__crop_and_ocr__(coords))
						case "rue":
							adresse.modifier_rue(self.__crop_and_ocr__(coords))
						case "complement":
							adresse.modifier_complement(self.__crop_and_ocr__(coords))
						case "boite_postale":
							adresse.modifier_boite_postale(self.__crop_and_ocr__(coords))
						case "code postal":
							adresse.modifier_code_postal(self.__crop_and_ocr__(coords))
						case "ville":
							adresse.modifier_ville(self.__crop_and_ocr__(coords))
						case "pays":
							adresse.modifier_pays(self.__crop_and_ocr__(coords))
				elif sous_parties[0] == "personne":
					match sous_parties[1]:
						case "nom":
							acheteur.modifier_nom(self.__crop_and_ocr__(coords))
						case "prenom":
							acheteur.modifier_prenom(self.__crop_and_ocr__(coords))

				elif sous_parties[0] == "entreprise":
					if len(sous_parties) == 3:
						if sous_parties[1] == "adresse":
							match sous_parties[2]:
								case "numero":
									enseigne.avoir_adresse().modifier_numero(self.__crop_and_ocr__(coords))
								case "rue":
									enseigne.avoir_adresse().modifier_rue(self.__crop_and_ocr__(coords))
								case "complement":
									enseigne.avoir_adresse().modifier_complement(self.__crop_and_ocr__(coords))
								case "boite_postale":
									enseigne.avoir_adresse().modifier_boite_postale(self.__crop_and_ocr__(coords))
								case "code postal":
									enseigne.avoir_adresse().modifier_code_postal(self.__crop_and_ocr__(coords))
								case "ville":
									enseigne.avoir_adresse().modifier_ville(self.__crop_and_ocr__(coords))
								case "pays":
									enseigne.avoir_adresse().modifier_pays(self.__crop_and_ocr__(coords))
					if len(sous_parties) == 2:
						if sous_parties[1] == "nom":
							enseigne.modifier_nom(self.__crop_and_ocr__(coords))
				elif sous_parties[0] == "date_achat":
					date_achat = datetime.datetime.strptime(self.__crop_and_ocr__(coords), "%d/%m/%Y")

				elif sous_parties[0] == "prix_ht" or sous_parties[0] == "prix_ttc":
					if sous_parties[0] == "prix_ht":
						prix_ht = float(self.__crop_and_ocr__(coords))
					else:
						prix_ttc = float(self.__crop_and_ocr__(coords))
				else:
					raise ValueError("Erreur")

			return Facture(acheteur, adresse, enseigne, prix_ht, prix_ttc, date_achat)
