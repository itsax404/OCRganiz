import datetime

from PIL import Image
import pytesseract

from backend.classes import Facture, Fiche_Paie
from backend.classes.bases import Personne
from backend.classes.bases.adresse import Adresse
from backend.classes.bases.entreprise import Entreprise

from backend.images.reconnaisseurs.adresse_reconnaisseur import Adresse_Reconnaisseur
from backend.images.reconnaisseurs.entreprise_reconnaisseur import Entreprise_Reconnaisseur
from backend.images.reconnaisseurs.personne_reconnaisseur import Personne_Reconnaisseur
import os


class Image_Processor:
	"""
	Permet de reconnaître les informations d'une image à l'aide de l'OCR
	"""

	def __init__(self, tesseract_dir: str) -> None:
		"""
		Initialise le reconnaisseur
		:param tesseract_dir: le chemin vers le dossier contenant l'exécutable de tesseract
		"""
		self.tesseract_dir = tesseract_dir
		self.adresse_reconnaisseur = Adresse_Reconnaisseur()
		self.entreprise_reconnaisseur = Entreprise_Reconnaisseur()
		self.personne_reconnaisseur = Personne_Reconnaisseur()

	def crop(self, image, coordonnées: tuple[int, int, int, int], path) -> Image:
		"""
		Permet de redimensionner un fichier avec les coordonnées fournies
		:param image: l'image en Pixmap à convertir en Image Pillow
		:type image: Pixmap
		:param coordonnées: les coordonnées de la zone à recadrer
		:type coordonnées: tuple[int, int, int, int]
		:param path: le chemin du dossier temporaire
		:type path: str
		:return: L'image recadrée
		:rtype: Image
		"""
		self.image = os.path.join(path, "output", "output_temp.jpg")
		image.save(self.image)
		image_pillow = Image.open(self.image)
		return image_pillow.crop(coordonnées)

	def crop_interface(self, image, coordonnées: tuple[int, int, int, int]) -> Image:
		"""
		Permet de recadrer une image avec les coordonnées fournies
		:param image: L'image à recadrer
		:type image: Image
		:param coordonnées: Les coordonnées où il faut recadrer
		:type coordonnées: tuple[int, int, int, int]
		:return: L'image recadrée
		:rtype: Image
		"""
		image_pillow = Image.open(image)
		return image_pillow.crop(coordonnées)

	def __ocr_cropped_image__(self, image: Image, lang: str = "fra") -> str:
		"""
		Permet de reconnaître le texte d'une image à l'aide de l'OCR
		:param image: l'image où il faut reconnaître le texte
		:type image: Image
		:param lang: la langue de l'image
		:type lang: str
		:return: Le texte reconnu
		:rtype: str
		"""
		pytesseract.pytesseract.tesseract_cmd = self.tesseract_dir
		return pytesseract.image_to_string(image, lang=lang)

	def __crop_and_ocr__(self, coordonnées: tuple[int, int, int, int], path, lang: str = "fra") -> str:
		"""
		Permet de recadrer une image et de reconnaître son contenu à l'aide de l'OCR
		:param coordonnées: les coordonnées de la zone à recadrer
		:type coordonnées: tuple[int, int, int, int]
		:param path: le chemin du dossier temporaire
		:type path: str
		:param lang: la langue de l'image
		:type lang: str
		:return: Le texte reconnu
		:rtype: str
		"""
		cropped_image = self.crop(self.image, coordonnées, path)
		return self.__ocr_cropped_image__(cropped_image, lang=lang)

	def reconnaitre(self, images, coordonnees, type, path):
		"""
		Permet de reconnaître les informations d'une image à l'aide de l'OCR
		:param images: les images à reconnaître
		:type images: list[Image]
		:param coordonnees: les coordonnées des zones à reconnaître
		:type coordonnees: list[tuple[int, int, int, int]]
		:param type: le type de document à reconnaître
		:type type: str
		:param path: le chemin du dossier temporaire
		:type path: str
		:return: les informations reconnues
		:rtype: dict

		Les différents types de données sont :
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
			adresse_entreprise = Adresse()
			enseigne = Entreprise()
			prix_ht = 0.0
			prix_ttc = 0.0
			date_achat = None
			for coordonnee in coordonnees:
				page = coordonnee["page"]
				self.image = images[page]
				sous_parties = [partie for partie in coordonnee["type"].split(".") if partie != ""]
				coords = coordonnee["coordonnées"]
				ocr = self.__crop_and_ocr__(coords, path).replace("\n", "")
				print(f"{sous_parties} | {ocr}")
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
					if len(sous_parties) == 4:
						if sous_parties[1] == "adresse":
							print(f"sous_partie = {sous_parties[2]}")
							match sous_parties[2]:
								case "numero":
									adresse_entreprise.modifier_numero(ocr)
								case "rue":
									adresse_entreprise.modifier_rue(ocr)
								case "complement":
									adresse_entreprise.modifier_complement(ocr)
								case "boite_postale":
									adresse_entreprise.modifier_boite_postale(ocr)
								case "code postal":
									adresse_entreprise.modifier_code_postal(ocr)
								case "ville":
									adresse_entreprise.modifier_ville(ocr)
								case "pays":
									adresse_entreprise.modifier_pays(ocr)
					if len(sous_parties) == 2:
						if sous_parties[1] == "nom":
							enseigne.modifier_nom(ocr)
				elif sous_parties[0] == "date_achat":
					date_achat = (ocr)

				elif sous_parties[0] == "prix_ht" or sous_parties[0] == "prix_ttc":
					if sous_parties[0] == "prix_ht":
						prix_ht = float(ocr.replace(",", "."))
					else:
						prix_ttc = float(ocr.replace(",", "."))
				else:
					raise ValueError("Erreur")

				a = os.path.join(path, "output", "output_temp.jpg")
				if os.path.isfile(a):
					os.remove(a)
			enseigne.modifier_adresse(adresse_entreprise)
			print(adresse.avoir_donnees())
			print(enseigne.avoir_adresse().avoir_donnees())
			return Facture(acheteur, adresse, enseigne, prix_ht, prix_ttc, date_achat)

		elif type == "fiche_de_paie":
			employé = Personne()
			enseigne = Entreprise(adresse=Adresse())
			revenu_net = 0.0
			revenu_brut = 0.0
			date_achat = None
			for coordonnee in coordonnees:
				page = coordonnee["page"]
				self.image = images[page]
				sous_parties = [partie for partie in coordonnee["type"].split(".") if partie != ""]
				coords = coordonnee["coordonnées"]
				ocr = self.__crop_and_ocr__(coords, path).replace("\n", "")
				if len(sous_parties) == 1:
					return None
				if sous_parties[0] == "personne":
					match sous_parties[1]:
						case "nom":
							employé.modifier_nom(ocr)
						case "prenom":
							employé.modifier_prenom(ocr)
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
				elif sous_parties[0] == "date":
					date_achat = ocr

				elif sous_parties[0] == "revenu_net" or sous_parties[0] == "revenu_brut":
					if sous_parties[0] == "reveu_net":
						revenu_net = float(ocr.replace(",", "."))
					else:
						revenu_brut = float(ocr.replace(",", "."))
				else:
					raise ValueError("Erreur")

				a = os.path.join(path, "output", "output_temp.jpg")
				if os.path.isfile(a):
					os.remove(a)
			return Fiche_Paie(employé, enseigne, revenu_net, revenu_brut, date_achat)
