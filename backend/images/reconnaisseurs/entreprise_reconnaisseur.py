from backend.images.reconnaisseurs import Reconnaisseur

from backend.images.reconnaisseurs.adresse_reconnaisseur import Adresse_Reconnaisseur
from backend.classes.bases.entreprise import Entreprise

class Entreprise_Reconnaisseur(Reconnaisseur):

	def __init__(self):
		self.nom = ""
		self.adresse = ""

	def reconnaitre(self, chaine):
		nom, adresse = chaine.split("\n")
		self.nom = nom
		self.adresse_reconnaisseur = Adresse_Reconnaisseur()
		self.adresse = self.adresse_reconnaisseur.reconnaitre(adresse)

	def avoir(self):
		return Entreprise(self.nom, self.adresse)