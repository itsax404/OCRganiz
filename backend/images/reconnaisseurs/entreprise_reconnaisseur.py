from backend.images.reconnaisseurs import Reconnaisseur

from backend.images.reconnaisseurs.adresse_reconnaisseur import Adresse_Reconnaisseur
from backend.classes.bases.entreprise import Entreprise

class Entreprise_Reconnaisseur(Reconnaisseur):

	def __init__(self) -> None:
		"""
		Pour créer un reconnaisseur d'entreprise
		:return: None
		:rtype: None
		"""
		self.nom = ""
		self.adresse = ""

	def reconnaitre(self, chaine: str) -> None:
		"""
		Pour reconnaitre une entreprise
		:param chaine: la chaîne de caractères à reconnaitre
		:type chaine: str
		:return: Rien
		:rtype: None
		"""
		nom, adresse = chaine.split("\n")
		self.nom = nom
		self.adresse_reconnaisseur = Adresse_Reconnaisseur()
		self.adresse = self.adresse_reconnaisseur.reconnaitre(adresse)

	def avoir(self) -> Entreprise:
		"""
		Permet d'obtenir la classe 'Entreprise' à partir des données reconnues
		:return: l'entreprise reconnue
		:rtype: Entreprise
		"""
		return Entreprise(self.nom, self.adresse)