from .bases.entreprise import Entreprise
from .bases.personne import Personne
import datetime


class Modele:

	def __init__(self, donnees) -> None:
		"""
        TODO
        """
		self.attributs = []
		self.nom = donnees[0]["nom_modele"]
		self.type = donnees[0]["type"]
		donnees.pop(0)
		for i, donnee in enumerate(donnees):
			coordonnees = donnee["coordonnées"]
			type_donnee = donnee["type"]
			page = donnee["page"]
			dictionnaire = {}
			setattr(self, f"rectangle_x{i + 1}_1", coordonnees[0])
			dictionnaire[f"rectangle_x{i + 1}_1"] = coordonnees[0]
			setattr(self, f"rectangle_x{i + 1}_2", coordonnees[2])
			dictionnaire[f"rectangle_x{i + 1}_2"] = coordonnees[2]
			setattr(self, f"rectangle_y{i + 1}_1", coordonnees[1])
			dictionnaire[f"rectangle_y{i + 1}_1"] = coordonnees[1]
			setattr(self, f"rectangle_y{i + 1}_2", coordonnees[3])
			dictionnaire[f"rectangle_y{i + 1}_2"] = coordonnees[3]
			setattr(self, f"page_rectangle{i + 1}", page)
			dictionnaire[f"page_rectangle{i+1}"] = page
			setattr(self, f"utilisation_rectangle{i + 1}", type_donnee)
			dictionnaire[f"utilisation_rectangle{i + 1}"] = type_donnee
			self.attributs.append(dictionnaire)

	def avoir_donnees(self):
		return self.attributs

	def avoir_nom(self):
		return self.nom

	def avoir_type(self):
		return self.type