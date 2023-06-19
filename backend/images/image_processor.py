from PIL import Image
import pytesseract

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

	def reconnaitre(self, coordonnees, objet):
		"""
		coordonnee : [{"coordonnées": (int, int, int, int), "type": "*.*" }]
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
		self.image = image
		if objet is None:
			for coordonnee in coordonnees:
				type_donnee = coordonnee["type"]
				sous_partie = list(type_donnee.split("."))
				if len(sous_partie) == 1:
					match type_donnee:
						case "adresse":
							self.adresse_reconnaisseur.reconnaitre(self.__crop_and_ocr__(coordonnee["coordonnées"]))
							return self.adresse_reconnaisseur.avoir()
						case "entreprise":
							self.entreprise_reconnaisseur.reconnaitre(self.__crop_and_ocr__(coordonnee["coordonnées"]))
							return self.entreprise_reconnaisseur.avoir()
						case "personne":
							self.personne_reconnaisseur.reconnaitre(self.__crop_and_ocr__(coordonnee["coordonnées"]))
							return self.personne_reconnaisseur.avoir()
						case "flottant":
							self.prix_reconnaisseur.reconnaitre(self.__crop_and_ocr__(coordonnee["coordonnées"]))
							return self.prix_reconnaisseur.avoir()
				else:
					raise ValueError("Il faut spécifier un objet pour le modifier")

		else:
			for coordonnee in coordonnees:
				type_donnee = coordonnee["type"]
				sous_parties = list(type_donnee.split("."))
				if len(sous_parties) == 1:
					match type_donnee:
						case "adresse":
							self.adresse_reconnaisseur.reconnaitre(self.__crop_and_ocr__(coordonnee["coordonnées"]))
							return self.adresse_reconnaisseur.avoir()
						case "entreprise":
							self.entreprise_reconnaisseur.reconnaitre(self.__crop_and_ocr__(coordonnee["coordonnées"]))
							return self.entreprise_reconnaisseur.avoir()
						case "personne":
							self.personne_reconnaisseur.reconnaitre(self.__crop_and_ocr__(coordonnee["coordonnées"]))
							return self.personne_reconnaisseur.avoir()
						case "flottant":
							self.prix_reconnaisseur.reconnaitre(self.__crop_and_ocr__(coordonnee["coordonnées"]))
							return self.prix_reconnaisseur.avoir()
				elif len(sous_parties) == 2:
					if (sous_parties[0] == "adresse") and (type(objet) == Adresse):
						adresse = objet
						match sous_parties[1]:
							case "numero":
								self.adresse_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
								nv_numero = self.adresse_reconnaisseur.avoir().avoir_numero()
								adresse.modifier_numero(nv_numero)
								return adresse
							case "rue":
								self.adresse_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
								nvlle_rue = self.adresse_reconnaisseur.avoir().avoir_rue()
								adresse.modifier_rue(nvlle_rue)
								return adresse
							case "boite_postale":
								self.adresse_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
								nvlle_boite = self.adresse_reconnaisseur.avoir().avoir_boite_postale()
								adresse.modifier_boite_postale(nvlle_boite)
								return adresse
							case "code_postal":
								self.adresse_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
								nv_cp = self.adresse_reconnaisseur.avoir().avoir_code_postal()
								adresse.modifier_code_postal(nv_cp)
								return adresse
							case "ville":
								self.adresse_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
								nvlle_ville = self.adresse_reconnaisseur.avoir().avoir_ville()
								adresse.modifier_ville(nvlle_ville)
								return adresse
							case "pays":
								self.adresse_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
								nv_pays = self.adresse_reconnaisseur.avoir().avoir_pays()
								adresse.modifier_pays(nv_pays)
								return adresse

					elif (sous_parties[0] == "entreprise") and (type(objet) == Entreprise):
						entreprise = objet
						match sous_parties[1]:
							case "nom":
								self.entreprise_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
								nv_nom = self.entreprise_reconnaisseur.avoir().avoir_nom()
								entreprise.modifier_nom(nv_nom)
								return entreprise
							case "adresse":
								self.adresse_reconnaisseur.reconnaitre(self.__crop_and_ocr__(coordonnee["coordonnées"]))
								return self.adresse_reconnaisseur.avoir()
					elif (sous_parties[0] == "personne") and (type(objet) == Entreprise):
						personne = objet
						match sous_parties[1]:
							case "nom":
								self.entreprise_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
								nv_nom = self.entreprise_reconnaisseur.avoir().avoir_nom()
								personne.modifier_nom(nv_nom)
								return personne
							case "prenom":
								self.entreprise_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
								nv_prenom = self.entreprise_reconnaisseur.avoir().avoir_prenom()
								personne.modifier_prenom(nv_prenom)
								return personne
					else:
						raise ValueError("L'objet fourni ne correspond pas à la valeur à modifier")

				elif len(sous_parties) == 3:
					if (sous_parties[0] != "entreprise") or (sous_parties[1] != "adresse"):
						raise ValueError("Mauvais identifiant de valeur fourni")
					if type(objet) != Entreprise:
						raise ValueError("L'objet fournir ne correspond aux valeurs à reconnaître")
					adresse = objet.avoir_adresse()
					match sous_parties[1]:
						case "numero":
							self.adresse_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
							nv_numero = self.adresse_reconnaisseur.avoir().avoir_numero()
							adresse.modifier_numero(nv_numero)
							entreprise.modifier_adresse(adresse)
							return entreprise
						case "rue":
							self.adresse_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
							nvlle_rue = self.adresse_reconnaisseur.avoir().avoir_rue()
							adresse.modifier_rue(nvlle_rue)
							entreprise.modifier_adresse(adresse)
							return entreprise
						case "boite_postale":
							self.adresse_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
							nvlle_boite = self.adresse_reconnaisseur.avoir().avoir_boite_postale()
							adresse.modifier_boite_postale(nvlle_boite)
							entreprise.modifier_adresse(adresse)
							return entreprise
						case "code_postal":
							self.adresse_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
							nv_cp = self.adresse_reconnaisseur.avoir().avoir_code_postal()
							adresse.modifier_code_postal(nv_cp)
							entreprise.modifier_adresse(adresse)
							return entreprise
						case "ville":
							self.adresse_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
							nvlle_ville = self.adresse_reconnaisseur.avoir().avoir_ville()
							adresse.modifier_ville(nvlle_ville)
							entreprise.modifier_adresse(adresse)
							return entreprise
						case "pays":
							self.adresse_reconnaisseur.reconnaitre(coordonnee["coordonnees"])
							nv_pays = self.adresse_reconnaisseur.avoir().avoir_pays()
							adresse.modifier_pays(nv_pays)
							entreprise.modifier_adresse(adresse)
							return entreprise
