from backend.images.reconnaisseurs.reconnaisseur import Reconnaisseur
import sys
from backend.classes.bases.personne import Personne
class Personne_Reconnaisseur(Reconnaisseur):

	def __init__(self):
		"""
		Permet de créer un reconnaisseur de personne
		:return: None
		:rtype: None
		"""
		self.nom = ""
		self.prenom = ""

	def vérifier_string(self, string: str) -> bool:
		"""
		Permet de vérifier si une chaine de caractère est valide
		:param string: la chaine de caractère à vérifier
		:type string: str
		:return: True si la chaine de caractère est valide, False sinon
		:rtype: bool
		"""
		for lettre in string:
			if not lettre.isalpha():
				return False
		return True

	def reconnaitre(self, chaine):
		"""
		Permet de reconnaitre une personne
		:param chaine: la chaine de caractère à
		:type chaine: str
		:return: Rien
		:rtype: None
		"""
		nom, prenom = chaine.split(" ")
		if not self.vérifier_string(nom):
			raise ValueError("Le nom n'est pas un nom valide")
		if not self.vérifier_string(prenom):
			raise ValueError("La prénom n'est pas un nom valide")
		self.nom = nom
		self.prenom = prenom

	def intervertir(self):
		"""
		Permet d'intervertir le nom et le prénom
		:return: Rien
		:rtype: None
		"""
		self.nom, self.prenom = self.prenom, self.nom

	def avoir(self):
		"""
		Permet d'obtenir la personne reconnue à partir de la chaine de caractères
		:return: la personne reconnue
		:rtype: Personne
		"""
		return Personne(self.prenom, self.nom)