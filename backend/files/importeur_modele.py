import os
import json
from backend.classes.modele import Modele


class Importateur():

	def __init__(self, path, database):
		self.database = database
		self.modele_dir = os.path.join(path, "modeles")
		if not os.path.isdir(self.modele_dir):
			os.mkdir(self.modele_dir)
		self.collecte_modeles()

	def collecte_modeles(self):
		"""
		TODO
		:return:
		"""
		fichiers = [fichier for fichier in os.listdir(self.modele_dir) if os.path.isfile(os.path.join(self.modele_dir, fichier))]
		for fichier in fichiers:
			extension = os.path.splitext(fichier)[-1].lower()

			if extension == ".modele":
				contenu_fichier = open(os.path.join(self.modele_dir, fichier)).read()
				modele = Modele(contenu_fichier)
				self.database.ajouter_modele(modele)