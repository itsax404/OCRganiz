from reconnaisseur import Reconnaisseur
import sys
sys.path.insert("D:\\Developpement\\Python\\projet-programmation\\backend\\images\\reconnaisseurs")

from personne import Personne

class Personne_Reconnaisseur(Reconnaisseur):

	def __init__(self):
		self.nom = ""
		self.prenom = ""

	def vérifier_string(self, string):
		for lettre in string:
			if not lettre.isalpha():
				return False
		return True

	def reconnaitre(self, chaine):
		nom, prenom = chaine.split(" ")
		if not self.vérifier_string(nom)
			raise ValueError("Le nom n'est pas un nom valide")
		if not self.vérifier_string(prenom):
			raise ValueError("La prénom n'est pas un nom valide")
		self.nom = nom
		self.prenom = prenom

	def intervertir(self):
		self.nom, self.prenom = self.prenom, self.nom

	def avoir(self):
		return Personne(self.prenom, self.nom)