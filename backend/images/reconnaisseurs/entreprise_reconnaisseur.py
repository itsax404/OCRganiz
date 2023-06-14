from reconnaisseur import Reconnaisseur

from adresse_reconnaisseur import Adresse_Reconnaisseur
sys.path.insert("D:\\Developpement\\Python\\projet-programmation\\backend\\images\\reconnaisseurs")

from entreprise import Entreprise

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