import os
from backend.classes.modele import Modele
from backend.database import Database


class Importateur():

	def __init__(self, path: str, database: Database) -> None:
		"""
		Permet d'importer les modèles du dossier 'modele'
		:param path: Le chemin de la racine du projet
		:param database:    La base de données
		"""
		self.database = database
		self.modele_dir = os.path.join(path, "modeles")
		if not os.path.isdir(self.modele_dir):
			os.mkdir(self.modele_dir)
		self.collecte_modeles()

	def collecte_modeles(self) -> None:
		"""
		Permet de lire les fichiers de modèles et de les ajouter à la base de données
		:return: Rien
		:rtype: None
		"""
		fichiers = [fichier for fichier in os.listdir(self.modele_dir) if os.path.isfile(os.path.join(self.modele_dir, fichier))]
		for fichier in fichiers:
			extension = os.path.splitext(fichier)[-1].lower()

			if extension == ".modele":
				contenu_fichier = open(os.path.join(self.modele_dir, fichier), encoding="UTF-8").read()
				contenu_nettoyé = json.loads(contenu_fichier)
				modele = Modele(contenu_nettoyé)
				self.database.ajouter_modele(modele)