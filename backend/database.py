import sqlite3
import os
from pathlib import Path
from classes.bases.adresse import Adresse
from classes.fiche_paie import Fiche_Paie
from classes.bases.personne import Personne
from classes.bases.entreprise import Entreprise
from classes.facture import Facture


class Database:

	def __init__(self) -> None:
		"""
		Permet de créer un objet "Database" qui permet de gérer la base de données.
		:return: Rien:
		:rtype: None
		"""
		self.connexion = sqlite3.connect(os.path.join(Path(__file__).parents[1], "database.db"))
		self.__creer_tables__()

	def __creer_tables__(self) -> None:
		"""
		Permet de créer les tables dans la base de données
		:return: Rien
		:rtype: None
		"""
		curseur = self.connexion.cursor()
		instructions_sql = [
			'CREATE TABLE IF NOT EXISTS adresses (id INTEGER PRIMARY KEY AUTOINCREMENT, numero TEXT, rue TEXT,'
			'complement TEXT, boite_postale TEXT, code_postal INT, ville TEXT, pays TEXT)',
			'CREATE TABLE IF NOT EXISTS personnes (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT)',
			'CREATE TABLE IF NOT EXISTS entreprises (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, adresse INT, '
			'FOREIGN KEY (adresse) REFERENCES adresses(id))',
			'CREATE TABLE IF NOT EXISTS factures (id INTEGER PRIMARY KEY AUTOINCREMENT, acheteur INT, adresse_acheteur '
			'INT, enseigne INT, prix_ht DOUBLE, prix_ttc DOUBLE, date_achat DATE, fichier LONGBLOB, FOREIGN KEY ('
			'acheteur) REFERENCES personnes(id), FOREIGN KEY (adresse_acheteur) REFERENCES adresses(id), FOREIGN KEY ('
			'enseigne) REFERENCES entreprises(id))',
			'CREATE TABLE IF NOT EXISTS fiches_paie (id INTEGER PRIMARY KEY AUTOINCREMENT, entreprise INT, '
			'employe INT, date DATE, revenu_brut DOUBLE, revenu_net DOUBLE, fichier LONGBLOB, FOREIGN KEY (entreprise) '
			'REFERENCES entreprises(id), FOREIGN KEY (employe) REFERENCES personnes(id) )',
			'CREATE TABLE IF NOT EXISTS modeles (nom_modele TEXT PRIMARY KEY, type TEXT ,'
			'rectangle_x1_1 FLOAT, rectangle_x1_2 FLOAT, rectangley1_1 FLOAT, rectangley1_2 FLOAT, '
			'utilisation_rectangle1 TEXT,rectangle_x2_1 FLOAT, rectangle_x2_2 FLOAT, rectangle_y2_1 FLOAT, '
			'rectangley2_2 FLOAT, utilisation_rectangle2 TEXT,rectangle_x3_1 FLOAT, rectangle_x3_2 FLOAT, '
			'rectangley3_1 FLOAT, rectangley3_2 FLOAT, utilisation_rectangle3 TEXT,rectangle_x4_1 FLOAT, '
			'rectangle_x4_2 FLOAT, rectangley4_1 FLOAT, rectangley4_2 FLOAT, utilisation_rectangle4 TEXT,'
			'rectangle_x5_1 FLOAT, rectangle_x5_2 FLOAT, rectangley5_1 FLOAT, rectangley5_2 FLOAT, '
			'utilisation_rectangle5 TEXT,rectangle_x6_1 FLOAT, rectangle_x6_2 FLOAT, rectangley6_1 FLOAT, '
			'rectangley6_2 FLOAT, utilisation_rectangle6 TEXT,rectangle_x7_1 FLOAT, rectangle_x7_2 FLOAT, '
			'rectangley7_1 FLOAT, rectangley7_2 FLOAT, utilisation_rectangle7 TEXT,rectangle_x8_1 FLOAT, '
			'rectangle_x8_2 FLOAT, rectangley8_1 FLOAT, rectangley8_2 FLOAT, utilisation_rectangle8 TEXT,'
			'rectangle_x9_1 FLOAT, rectangle_x9_2 FLOAT, rectangley9_1 FLOAT, rectangley9_2 FLOAT, '
			'utilisation_rectangle9 TEXT,rectangle_x10_1 FLOAT, rectangle_x10_2 FLOAT, rectangley10_1 FLOAT, '
			'rectangley10_2 FLOAT, utilisation_rectangle10 TEXT,rectangle_x11_1 FLOAT, rectangle_x11_2 FLOAT, '
			'rectangley11_1 FLOAT, rectangley11_2 FLOAT, utilisation_rectangle11 TEXT,rectangle_x12_1 FLOAT, '
			'rectangle_x12_2 FLOAT, rectangley12_1 FLOAT, rectangley12_2 FLOAT, utilisation_rectangle12 TEXT,'
			'rectangle_x13_1 FLOAT, rectangle_x13_2 FLOAT, rectangley13_1 FLOAT, rectangley13_2 FLOAT, '
			'utilisation_rectangle13 TEXT,rectangle_x14_1 FLOAT, rectangle_x14_2 FLOAT, rectangley14_1 FLOAT, '
			'rectangley14_2 FLOAT, utilisation_rectangle14 TEXT)'
		]
		for instruction in instructions_sql:
			curseur.execute(instruction)
		self.connexion.commit()
		curseur.close()

	# <============ PARTIE ADRESSE ============>

	def ajouter_adresse(self, adresse: Adresse) -> Adresse:
		"""
		Permet d'ajouter une adresse dans la base de données
		:param adresse: l'adresse à ajouter
		:type adresse: Adresse
		:return: l'adresse avec l'identifiant de la base de données
		:rtype: Adresse
		"""
		if self.est_dans_la_base_adresse(adresse.id):
			return self.avoir_adresse(adresse.id)
		curseur = self.connexion.cursor()
		curseur.execute(
			'INSERT INTO adresses (numero, rue, complement, boite_postale, code_postal, ville, pays) VALUES (?, ?, ?, ?, ?, ?,  ?, ?)',
			tuple(adresse.avoir_donnees().values()))
		self.connexion.commit()
		donnees = adresse.avoir_donnees()
		nouvelle_adresse = Adresse(donnees["numero_rue"], donnees["adresse"], donnees["complement"],
		                           donnees["boite_postale"], donnees["code_postal"], donnees["ville"], donnees["pays"],
		                           curseur.lastrowid)
		curseur.close()
		return nouvelle_adresse

	def avoir_adresse(self, id: int) -> Adresse | None:
		"""
		Permet d'avoir une adresse à partie de son identifiant
		:param id: l'identifiant de l'adresse
		:type id: int
		:return: l'adresse ou None si elle n'est pas dans la base de données
		:rtype: Adresse | None
		"""
		if not self.est_dans_la_base_adresse(id):
			return None
		curseur = self.connexion.cursor()
		curseur.execute('SELECT * FROM adresses WHERE id = ?', (id,))
		resultat = curseur.fetchone()
		curseur.close()
		return Adresse(resultat[1], resultat[2], resultat[3], resultat[4], resultat[5], resultat[6], resultat[0])

	def est_dans_la_base_adresse(self, id: int) -> bool:
		"""
		Permet de savoir si une adresse est dans la base de données
		:param id: l'identifiant à vérifier
		:return: Si une adresse est dans la base de données ou non
		:rtype: bool
		"""
		curseur = self.connexion.cursor()
		curseur.execute('SELECT * FROM adresses WHERE id = ?', (id,))
		resultat = curseur.fetchone()
		curseur.close()
		return resultat is not None

	def avoir_identifiant_adresse(self, adresse: Adresse) -> int | None:
		"""
		Permet d'obtenir l'identifiant d'une adresse
		:param adresse: l'adresse à avoir l'identifiant
		:return: l'identifiant ou None si elle n'est pas dans la base ed données
		:rtype: int ou None
		"""
		adresses = self.avoir_toutes_les_adresses()
		for adresse_de_la_base in adresses:
			if adresse_de_la_base == adresse:
				return adresse_de_la_base.avoir_identifiant()
		return None

	def avoir_toutes_les_adresses(self) -> list[Adresse]:
		"""
		Permet d'avoir toutes les adresses de la base de données
		:return: la liste de toutes les adresses
		:rtype: list[Adresse]
		"""
		curseur = self.connexion.cursor()
		curseur.execute('SELECT * FROM adresses')
		resultat = curseur.fetchall()
		adresses = []
		for adresse in resultat:
			adresse_classe = Adresse(adresse[1], adresse[2], adresse[3], adresse[4], adresse[5], adresse[6], adresse[0])
			adresses.append(adresse_classe)
		curseur.close()
		return adresses

	def modifier_adresse(self, id: int, nouvelle_adresse: Adresse) -> Adresse | None:
		"""
		Permet de modifier une adresse
		:param id: l'identifiant de l'adresse à modifier
		:type id: int
		:param nouvelle_adresse: la classe "adresse" avec les nouvelles données
		:type nouvelle_adresse: Adresse
		:return: l'adresse avec l'identifiant ou None si elle n'est pas dans la base de données
		:rtype: Adresse | None
		"""
		if not self.est_dans_la_base_adresse(id):
			return None
		curseur = self.connexion.cursor()
		curseur.execute(
			"UPDATE adresses SET numero = ?, rue = ?, complement = ?, boite_postale = ?, code_postal = ?, ville = ? , pays = ? WHERE id = ?",
			tuple(nouvelle_adresse.avoir_donnees().values()) + (id,))
		self.connexion.commit()
		curseur.close()
		return self.avoir_adresse(id)

	def supprimer_adresse(self, id: int) -> None:
		"""
		Permet de supprimer une adresse
		:param id: l'identifiant de l'adresse à supprimer
		:type id: int
		:return: Rien
		:rtype: None
		"""
		if not self.est_dans_la_base_adresse(id):
			return None
		curseur = self.connexion.cursor()
		curseur.execute("DELETE FROM adresses WHERE id = ?", (id,))
		self.connexion.commit()
		curseur.close()

	# <============ PARTIE PERSONNE ============>

	def ajouter_personne(self, personne: Personne) -> Personne:
		"""
		Permet d'ajouter une personne à la base de données
		:param personne: La personne à ajouter
		:type personne: Personne
		:return: la classe avec l'identifiant
		"""
		if self.est_dans_la_base_personne(personne.avoir_identifiant()):
			return self.avoir_personne(personne.avoir_identifiant())
		curseur = self.connexion.cursor()
		curseur.execute('INSERT INTO personnes (nom, prenom) VALUES (?, ?, ?, ?)',
		               tuple(personne.avoir_donnees().values()))
		self.connexion.commit()
		donnees = personne.avoir_donnees()
		nouvelle_personne = Personne(donnees["nom"], donnees["prenom"], curseur.lastrowid)
		curseur.close()
		return nouvelle_personne

	def avoir_personne(self, id: int) -> Personne | None:
		"""
		Permet d'obtenir une personne de la base de données
		:param id: l'identifiant de la personne à obtenir
		:type id: int
		:return: la classe personne ou None si elle n'est pas dans la base de données
		:rtype: Personne ou None
		"""
		if not self.est_dans_la_base_personne(id):
			return None
		curseur = self.connexion.cursor()
		curseur.execute('SELECT * FROM personnes WHERE id = ?', (id,))
		resultat = curseur.fetchone()
		curseur.close()
		return Personne(resultat[1], resultat[2], resultat[0])

	def est_dans_la_base_personne(self, id: int) -> bool:
		"""
		Permet de savoir si une personne est dans la base de données
		:param id: l'identifiant de la personne à vérifier
		:type id: int
		:return: True si elle est dans la base de données, False sinon
		:rtype: bool
		"""
		curseur = self.connexion.cursor()
		curseur.execute('SELECT * FROM personnes WHERE id = ?', (id,))
		resultat = curseur.fetchone()
		curseur.close()
		return resultat is not None

	def avoir_identifiant_personne(self, personne: Personne) -> int:
		"""
		Permet d'avoir l'identifiant d'une personne
		:param personne: la personne dont on veut l'identifiant
		:type personne: Personne
		:return: l'identifiant de la personne ou None si elle n'est pas dans la base de données
		:rtype: int ou None
		"""
		personnes = self.avoir_toutes_les_personnes()
		for personne_de_la_base in personnes:
			if personne_de_la_base == personne:
				return personne_de_la_base.avoir_identifiant()
		return None

	def avoir_toutes_les_personnes(self) -> list[Personne]:
		"""
		Permet d'avoir toutes les personnes de la base de données
		:return: la liste des personnes
		:rtype: list[Personne]
		"""
		curseur = self.connexion.cursor()
		curseur.execute('SELECT * FROM personnes')
		resultat = curseur.fetchall()
		personnes = []
		for personne in resultat:
			personnes.append(Personne(personne[1], personne[2], personne[0]))
		curseur.close()
		return personnes

	def modifier_personne(self, id: int, nouvelle_personne: Personne) -> Personne | None:
		"""
		Permet de modifier une personne
		:param id: identifiant de la personne à modifier
		:param nouvelle_personne: la classe "Personne" avec les nouvelles données
		:return: la classe "Personne" avec les nouvelles données ou None si elle n'est pas dans la base de données
		:rtype: Personne ou None
		"""
		if not self.est_dans_la_base_personne(id):
			return None
		curseur = self.connexion.cursor()
		curseur.execute("UPDATE personnes SET nom = ?, prenom = ? WHERE id = ?",
		               tuple(nouvelle_personne.avoir_donnees().values()) + (id,))
		self.connexion.commit()
		curseur.close()
		return self.avoir_personne(id)

	def supprimer_personne(self, id: int) -> None:
		"""
		Permet de supprimer une personne de la base de données
		:param id: l'id de la personne à supprimer
		:type id: int
		:return: Rien
		:rtype: None
		"""
		if not self.est_dans_la_base_personne(id):
			return None
		curseur = self.connexion.cursor()
		curseur.execute("DELETE FROM personnes WHERE id = ?", (id,))
		self.connexion.commit()
		curseur.close()

	# <============ PARTIE ENTREPRISE ============>

	def ajouter_entreprise(self, entreprise: Entreprise) -> Entreprise:
		"""
		Permet d'ajouter une entreprise dans la base de données
		Et renvoie un objet "Entreprise" avec l'identifiant de la base de données dans celle-ci
		:param entreprise: L'entreprise à ajouter
		:type entreprise: Entreprise
		:return: l'entreprise avec l'identifiant de la base de données
		:rtype: Entreprise
		"""
		curseur = self.connexion.cursor()
		if self.est_dans_la_base_entreprise(entreprise.avoir_identifiant()):
			return self.avoir_entreprise(entreprise.avoir_identifiant())
		adresse_entreprise = entreprise.adresse
		adresse_bdd = self.ajouter_adresse(adresse_entreprise)
		curseur.execute("INSERT INTO entreprises (nom, adresse) VALUES (?, ?)",
		                 tuple((entreprise.avoir_nom(), adresse_bdd.avoir_identifiant())))
		donnees = entreprise.avoir_donnees()
		entreprise_classe = Entreprise(donnees["nom"], adresse_bdd, curseur.lastrowid)
		self.connexion.commit()
		curseur.close()
		return entreprise_classe

	def avoir_entreprise(self, id: int) -> Entreprise:
		"""
		Permet d'avoir une entreprise de la base de données
		:param id: l'identifiant de l'entreprise
		:type id: int
		:return: l'objet Entreprise correspondant à l'identifiant
		:rtype: Entreprise
		"""
		curseur = self.connexion.cursor()
		curseur.execute("SELECT * FROM entreprises WHERE id = ?", (id,))
		resultat = curseur.fetchone()
		if resultat is None:
			return None
		adresse = self.avoir_adresse(resultat[2])
		return Entreprise(resultat[1], adresse, resultat[0])

	def avoir_identifiant_entreprise(self, entreprise: Entreprise) -> int:
		"""
		Permet d'avoir l'identifiant d'une entreprise dans la base de données
		:param entreprise: l'entreprise dont on veut l'identifiant
		:type entreprise: Entreprise
		:return: l'identifiant de l'entreprise dans la base de données
		:rtype: int
		"""
		entreprises = self.avoir_toutes_les_entreprises()
		for entreprise_de_la_base in entreprises:
			if entreprise_de_la_base == entreprise:
				return entreprise_de_la_base.avoir_identifiant()
		return None

	def avoir_toutes_les_entreprises(self) -> list[Entreprise]:
		"""
		Permet d'avoir toutes les entreprises de la base de données
		:return: une liste des entreprises dans la base de données
		:rtype: list[Entreprise]
		"""
		curseur = self.connexion.cursor()
		curseur.execute("SELECT * FROM entreprises")
		resultat = curseur.fetchall()
		entreprises = list()
		for entreprise in resultat:
			adresse_classe = self.avoir_adresse(entreprise[2])
			entreprise_classe = Entreprise(entreprise[1], adresse_classe, entreprise[0])
			entreprises.append(entreprise_classe)
		curseur.close()
		return entreprises

	def modifier_entreprise(self, id: int, nouvelle_entreprise: Entreprise) -> Entreprise:
		"""
		Permet de modifier une entreprise dans la base de données
		:param id: l'identifiant de l'entreprise à modifier
		:type id: int
		:param nouvelle_entreprise: l'objet Entreprise avec les nouvelles données
		:type nouvelle_entreprise: Entreprise
		:return: l'entreprise modifiée avec l'identifiant fourni
		:rtype: Entreprise
		"""
		if not self.est_dans_la_base_entreprise(id):
			return None
		nouvelle_adresse = self.ajouter_adresse(nouvelle_entreprise.avoir_adresse())
		curseur = self.connexion.cursor()
		curseur.execute("UPDATE entreprises SET nom = ?, adresse = ? WHERE id = ?",
		                (nouvelle_entreprise.avoir_nom, nouvelle_adresse.avoir_identifiant(), id))
		self.connexion.commit()
		curseur.close()
		return self.avoir_entreprise(id)

	def supprimer_entreprise(self, id: int) -> None:
		"""
		Permet de supprimer une entreprise
		:param id: l'identifiant de l'entreprise à supprimer
		:type id: int
		:return: Rien
		:rtype: None
		"""
		curseur = self.connexion.cursor()
		if not self.est_dans_la_base_entreprise(id):
			return None
		curseur.execute("DELETE FROM entreprises WHERE id = ?", (id,))
		self.connexion.commit()
		curseur.close()

	def est_dans_la_base_entreprise(self, id: int) -> bool:
		"""
		Permet de savoir si une entreprise est dans la base de données
		:param id: l'identifiant de l'entreprise
		:type id: int
		:return: Si l'entreprise est dans la base de données
		:rtype: bool
		"""
		curseur = self.connexion.cursor()
		curseur.execute("SELECT * FROM entreprises WHERE id = ?", (id,))
		resultat = curseur.fetchone()
		curseur.close()
		return resultat is not None

	# <============ PARTIE FACTURE ============>

	def ajouter_facture(self, facture: Facture) -> Facture:
		"""
		Permet d'ajouter une facture
		:param facture: la facture à ajouter
		:type facture: Facture
		:return: la facture ajoutée avec l'identifiant
		:rtype: Facture
		"""
		donnees = facture.avoir_donnees()
		donnees["adresse_acheteur"] = self.ajouter_adresse(donnees["adresse_acheteur"]).avoir_identifiant()
		donnees["enseigne"] = self.ajouter_entreprise(donnees["enseigne"]).avoir_identifiant()
		donnees["acheteur"] = self.ajouter_personne(donnees["acheteur"]).avoir_identifiant()
		curseur = self.connexion.cursor()
		curseur.execute(
			'INSERT INTO factures (acheteur, adresse_acheteur, enseigne, prix_ht, prix_ttc, date_achat, fichier) VALUES (?, ?, ?, ?, ?, ?, ?)',
			tuple(donnees.values()))
		self.connexion.commit()
		curseur.close()
		return self.avoir_facture(curseur.lastrowid)

	def avoir_facture(self, id: int) -> Facture | None:
		"""
		Permet d'avoir une facture à partir de son identifiant
		:param id: L'identifiant de la facture à chercher
		:type id: int
		:return: La facture trouvée ou None si elle n'existe pas
		:rtype: Facture ou None
		"""
		curseur = self.connexion.cursor()
		curseur.execute("SELECT * FROM factures WHERE id = ?", (id,))
		resultat = curseur.fetchone()
		if resultat is None:
			return None
		acheteur = self.avoir_personne(resultat[1])
		adresse_acheteur = self.avoir_adresse(resultat[2])
		enseigne = self.avoir_entreprise(resultat[3])
		return Facture(acheteur, adresse_acheteur, enseigne, resultat[4], resultat[5], resultat[6], resultat[7],
		               resultat[0])

	def avoir_identifiant_facture(self, facture: Facture) -> int | None:
		"""
		Permet d'avoir l'identifiant d'une facture
		:param facture: La facture dont on veut l'identifiant
		:return: l'identifiant de la facture ou None si elle n'existe pas
		:rtype: int ou None
		"""
		factures = self.avoir_toutes_les_factures()
		for facture_de_la_base in factures:
			if facture_de_la_base == facture:
				return facture_de_la_base.avoir_identifiant()
		return None

	def avoir_toutes_les_factures(self) -> list[Facture]:
		"""
		Permet d'avoir toutes les factures de la base de données
		:return: une liste de factures étant dans la base de données
		"""
		curseur = self.connexion.cursor()
		curseur.execute("SELECT * FROM factures")
		resultat = curseur.fetchall()
		factures = list()
		for facture in resultat:
			acheteur = self.avoir_personne(facture[1])
			adresse_acheteur = self.avoir_adresse(facture[2])
			enseigne = self.avoir_entreprise(facture[3])
			facture_classe = Facture(acheteur, adresse_acheteur, enseigne, facture[4], facture[5], facture[6],
			                         facture[7], facture[0])
			factures.append(facture_classe)
		curseur.close()
		return factures

	def modifier_facture(self, id: int, nouvelle_facture: Facture) -> Facture | None:
		"""
		Premet de modifier une facture
		:param id: l'identifiant de la facture à modifier
		:type id: int
		:param nouvelle_facture: la facture avec les nouvelles données
		:type nouvelle_facture: Facture
		:return: la facture modifiée avec son identifiant
		:rtype: Facture ou None
		"""
		if not self.est_dans_la_base_facture(id):
			return None
		nouvelle_adresse_acheteur = self.ajouter_adresse(nouvelle_facture.avoir_adresse_acheteur())
		nouvelle_enseigne = self.ajouter_entreprise(nouvelle_facture.avoir_enseigne())
		nouvel_acheteur = self.ajouter_personne(nouvelle_facture.avoir_acheteur())
		curseur = self.connexion.cursor()
		curseur.execute(
			"UPDATE factures SET acheteur = ?, adresse_acheteur = ?, enseigne = ?, prix_ht = ?, prix_ttc = ?, date_achat = ?, fichier = ? WHERE id = ?",
			(nouvel_acheteur.avoir_identifiant(), nouvelle_adresse_acheteur.avoir_identifiant(),
			 nouvelle_enseigne.avoir_identifiant(), nouvelle_facture.avoir_prix_ht(), nouvelle_facture.avoir_prix_ttc(),
			 nouvelle_facture.avoir_date_achat(), nouvelle_facture.avoir_fichier(), id))
		self.connexion.commit()
		curseur.close()
		return self.avoir_facture(id)

	def supprimer_facture(self, id: int) -> None:
		"""
		Permet de supprimer une facture
		:param id: l'identifiant de la facture à supprimer
		:type id: int
		:return: Rien
		:rtype: None
		"""
		if not self.est_dans_la_base_facture(id):
			return None

		curseur = self.connexion.cursor()
		curseur.execute("DELETE FROM factures WHERE id = ?", (id,))
		self.connexion.commit()
		curseur.close()

	def est_dans_la_base_facture(self, id: int) -> bool:
		"""
		Permet de savoir si une facture est dans la base de données
		:param id: l'identifiant de la facture
		:type id: int
		:return: Si la facture est dans la base de données
		:rtype: bool
		"""
		curseur = self.connexion.cursor()
		curseur.execute("SELECT * FROM factures WHERE id = ?", (id,))
		resultat = curseur.fetchone()
		curseur.close()
		return resultat is not None

	# <============ PARTIE FICHE DE PAIE ============>

	def ajouter_fiche_paie(self, fiche_paie: Fiche_Paie) -> Fiche_Paie:
		"""
		Permet d'ajouter une fiche de paie dans la base de données
		:param fiche_paie: la fiche de paie à ajouter
		:type fiche_paie: Fiche_Paie
		:return: la fiche de paie avec son identifiant
		:rtype: Fiche_Paie
		"""
		donnees = fiche_paie.avoir_donnees()
		entreprise_bdd = self.ajouter_entreprise(donnees["entreprise"])
		personne_bdd = self.ajouter_personne(donnees["employé"])
		donnees["entreprise"] = entreprise_bdd.avoir_identifiant()
		donnees["employé"] = personne_bdd.avoir_identifiant()
		curseur = self.connexion.cursor()
		curseur.execute(
			'INSERT INTO fiches_paie (entreprise, employe, date, revenu_brut, revenu_net, fichier) VALUES (?, ?, ?, ?, ?, ?)',
			tuple(donnees.values()))
		self.connexion.commit()
		curseur.close()
		return self.avoir_fiche_paie(curseur.lastrowid)

	def avoir_fiche_paie(self, id: int) -> Fiche_Paie | None:
		"""
		Permet d'avoir une fiche de paie
		:param id: l'identifiant de la fiche de paie
		:type id: int
		:return: la fiche de paie ou None si elle n'est pas dans la base de données
		:rtype: Fiche_Paie ou None
		"""
		curseur = self.connexion.cursor()
		curseur.execute("SELECT * FROM fiches_paie WHERE id = ?", (id,))
		resultat = curseur.fetchone()
		curseur.close()
		if resultat is None:
			return None
		entreprise = self.avoir_entreprise(resultat[1])
		employe = self.avoir_personne(resultat[2])
		return Fiche_Paie(entreprise, employe, resultat[3], resultat[4], resultat[5], resultat[6], resultat[0])

	def avoir_identifiant_fiche_paie(self, fiche_paie: Fiche_Paie) -> int | None:
		"""
		Permet d'avoir l'identifiant d'une fiche de paie
		:param fiche_paie: la fiche de paie
		:type fiche_paie: Fiche_Paie
		:return: l'identifiant de la fiche de paie ou None si elle n'est pas dans la base de données
		:rtype: int ou None
		"""
		fiches_paie = self.avoir_toutes_les_fiches_de_paie()
		for fiche_paie_de_la_base in fiches_paie:
			if fiche_paie_de_la_base == fiche_paie:
				return fiche_paie_de_la_base.avoir_identifiant()
		return None

	def avoir_toutes_les_fiches_de_paie(self) -> list[Fiche_Paie]:
		"""
		Permet d'avoir toutes les fiches de paie de la base de données
		:return: la liste des fiches de paie de la base de données
		:rtype: list[Fiche_Paie]
		"""
		curseur = self.connexion.cursor()
		curseur.execute("SELECT * FROM fiches_paie")
		resultat = curseur.fetchall()
		fiches_paie = list()
		for fiche_paie in resultat:
			entreprise = self.avoir_entreprise(fiche_paie[1])
			employe = self.avoir_personne(fiche_paie[2])
			date = fiche_paie[3]
			revenu_brut = fiche_paie[4]
			revenu_net = fiche_paie[5]
			fichier = fiche_paie[6]
			id = fiche_paie[0]
			fiche_paie_classe = Fiche_Paie(entreprise, employe, date, revenu_brut, revenu_net, fichier, id)
			fiches_paie.append(fiche_paie_classe)
		curseur.close()
		return fiches_paie

	def modifier_fiche_paie(self, id: int, nouvelle_fiche_paie: Fiche_Paie) -> Fiche_Paie | None:
		"""
		Permet de modifier une fiche de paie
		:param id: l'identifiant de la fiche de paie
		:type id: int
		:param nouvelle_fiche_paie: la fiche de paie contenant les nouvelles données
		:type nouvelle_fiche_paie: Fiche_Paie
		:return: la fiche de paie modifiée avec l'identifiant ou None si elle n'est pas dans la base de données
		:rtype: Fiche_Paie ou None
		"""
		if not self.est_dans_la_base_fiche_paie(id):
			return None
		donnees = nouvelle_fiche_paie.avoir_donnees()
		donnees["entreprise"] = self.modifier_entreprise(donnees["entreprise"]).avoir_identifiant()
		donnees["employé"] = self.modifier_personne(donnees["employé"]).avoir_identifiant()
		curseur = self.connexion.cursor()
		curseur.execute(
			'UPDATE fiches_paie SET entreprise = ?, employe = ?, date = ?, revenu_brut = ?, revenu_net = ?, fichier = ? WHERE id = ?',
			tuple(donnees.values()))
		self.connexion.commit()
		curseur.close()
		return self.avoir_fiche_paie(id)

	def supprimer_fiche_paie(self, id: int) -> None:
		"""
		Permet de supprimer une fiche de paie
		:param id: l'identifiant de la fiche de paie à supprimer
		:type id: int
		:return: Rien
		:rtype: None
		"""
		if not self.est_dans_la_base_fiche_paie(id):
			return None
		curseur = self.connexion.cursor()
		curseur.execute("DELETE FROM fiches_paie WHERE id = ?", (id,))
		self.connexion.commit()
		curseur.close()

	def est_dans_la_base_fiche_paie(self, id: int) -> bool:
		"""
		Permet de savoir si une fiche de paie est dans la base de données
		:param id: l'identifiant de la fiche de paie
		:type id: int
		:return: Si la fiche de paie est dans la base de données ou pas
		:rtype: bool
		"""
		curseur = self.connexion.cursor()
		curseur.execute("SELECT * FROM fiches_paie WHERE id = ?", (id,))
		resultat = curseur.fetchone()
		curseur.close()
		return resultat is not None

	# <============ PARTIE MODELE ============>

    	def ajouter_modele(self, modele: Modele) -> Modele:
		"""
		Permet d'ajouter une entreprise dans la base de données
		Et renvoie un objet "Entreprise" avec l'identifiant de la base de données dans celle-ci
		:param entreprise: L'entreprise à ajouter
		:type entreprise: Entreprise
		:return: l'entreprise avec l'identifiant de la base de données
		:rtype: Entreprise
		"""
		curseur = self.connexion.cursor()
        if self.est_deja_existant(modele.avoir_nom())
            return self.avoir_modele(entreprise.avoir_nom())
        string_bdd = "INSERT INTO modeles ("
        values = [modele.avoir_nom().lower()]
        for i, donnee in enumerate(modele.avoir_donnee()):
        	string_temp = f"rectangle_x{i}_1, rectangle_x{i}_2, rectangle_y{i}_1, rectangle_y{i}_2, utilisation_reactangle{i+1}"
			if i != (len(modele.avoir_donnee()) - 1):
				string_temp += ", "
        	values.append(donnee[f"rectangle_x{i + 1}_1"])        			values.append(donnee[f"rectangle_x{i + 1}_2"])        			values.append(donnee[f"rectangle_y{i + 1}_1"])        
          	values.append(donnee[f"rectangle_y{i + 1}_2"])
			values.append(donnee[f"type_{i + 1}]"])
		string_temp += " VALUES ()"
		for i in range(len(values)):
			if i == (len(values) - 1):
				string_temp += "?)"
			string_temp += "?,"
		self.connexion.commit()
		curseur.close()
		return modele

	def avoir_entreprise(self, nom: str) -> Entreprise:
		"""
		Permet d'avoir une entreprise de la base de données
		:param id: l'identifiant de l'entreprise
		:type id: int
		:return: l'objet Entreprise correspondant à l'identifiant
		:rtype: Entreprise
		"""
		curseur = self.connexion.cursor()
		curseur.execute("SELECT * FROM entreprises WHERE id = ?", (id,))
		resultat = curseur.fetchone()
		if resultat is None:
			return None
		adresse = self.avoir_adresse(resultat[2])
		return Entreprise(resultat[1], adresse, resultat[0])

	def avoir_identifiant_entreprise(self, entreprise: Entreprise) -> int:
		"""
		Permet d'avoir l'identifiant d'une entreprise dans la base de données
		:param entreprise: l'entreprise dont on veut l'identifiant
		:type entreprise: Entreprise
		:return: l'identifiant de l'entreprise dans la base de données
		:rtype: int
		"""
		entreprises = self.avoir_toutes_les_entreprises()
		for entreprise_de_la_base in entreprises:
			if entreprise_de_la_base == entreprise:
				return entreprise_de_la_base.avoir_identifiant()
		return None

	def avoir_toutes_les_entreprises(self) -> list[Entreprise]:
		"""
		Permet d'avoir toutes les entreprises de la base de données
		:return: une liste des entreprises dans la base de données
		:rtype: list[Entreprise]
		"""
		curseur = self.connexion.cursor()
		curseur.execute("SELECT * FROM entreprises")
		resultat = curseur.fetchall()
		entreprises = list()
		for entreprise in resultat:
			adresse_classe = self.avoir_adresse(entreprise[2])
			entreprise_classe = Entreprise(entreprise[1], adresse_classe, entreprise[0])
			entreprises.append(entreprise_classe)
		curseur.close()
		return entreprises

	def modifier_entreprise(self, id: int, nouvelle_entreprise: Entreprise) -> Entreprise:
		"""
		Permet de modifier une entreprise dans la base de données
		:param id: l'identifiant de l'entreprise à modifier
		:type id: int
		:param nouvelle_entreprise: l'objet Entreprise avec les nouvelles données
		:type nouvelle_entreprise: Entreprise
		:return: l'entreprise modifiée avec l'identifiant fourni
		:rtype: Entreprise
		"""
		if not self.est_dans_la_base_entreprise(id):
			return None
		nouvelle_adresse = self.ajouter_adresse(nouvelle_entreprise.avoir_adresse())
		curseur = self.connexion.cursor()
		curseur.execute("UPDATE entreprises SET nom = ?, adresse = ? WHERE id = ?",
		                (nouvelle_entreprise.avoir_nom, nouvelle_adresse.avoir_identifiant(), id))
		self.connexion.commit()
		curseur.close()
		return self.avoir_entreprise(id)

	def supprimer_entreprise(self, id: int) -> None:
		"""
		Permet de supprimer une entreprise
		:param id: l'identifiant de l'entreprise à supprimer
		:type id: int
		:return: Rien
		:rtype: None
		"""
		curseur = self.connexion.cursor()
		if not self.est_dans_la_base_entreprise(id):
			return None
		curseur.execute("DELETE FROM entreprises WHERE id = ?", (id,))
		self.connexion.commit()
		curseur.close()

    def est_deja_existant(self, nom: str):
        """
        """
        curseur = self.connexion.cursor()
        curseur.execute("SELECT * FRIL modeles WHERE nom = ?", (nom.lower(), ))
        resultat = curseur.fetchone()
        curseur.close()
        return resultat is not None

    
        
