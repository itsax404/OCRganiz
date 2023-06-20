from .bases.entreprise import Entreprise
from .bases.personne import Personne
import datetime


class Modele:

	def __init__(self, donnees: dict) -> None:
		"""
        Permet de créer la classe Modele qui permet de créer des modèles de documents
        :param donnees: Dictionnaire contenant les données du modèle
        :type donnees: dict
        :return: None
        :rtype: None
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

	def avoir_donnees(self) -> list[dict]:
		"""
		Permet d'obtenir les données du modèle
		:return: les attributs du modèle
		:rtype: list[dict]
		"""
		return self.attributs

	def avoir_nom(self) -> str:
		"""
		Permet d'obtenir le nom du modèle
		:return: le nom du modèle
		:rtype: str
		"""
		return self.nom

	def avoir_type(self) -> str:
		"""
		Permet d'obtenir le type du modèle
		:return: le type du modèle
		:rtype: str
		"""
		return self.type