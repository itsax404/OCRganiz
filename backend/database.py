import sqlite3
import os
from pathlib import Path
from classes.bases.adresse import Adresse
from classes.fiche_paie import Fiche_Paie
from classes.bases.personne import Personne
from classes.bases.entreprise import Entreprise
from classes.facture import Facture


class Database:

	def __init__(self):
		"""
		TODO docstring
		"""
		self.connexion = sqlite3.connect(os.path.join(Path(__file__).parents[1], "database.db"))
		self.__creer_tables__()

	def __creer_tables__(self):
		cursor = self.connexion.cursor()
		instructions_sql = [
			'CREATE TABLE IF NOT EXISTS adresses (id INTEGER PRIMARY KEY AUTOINCREMENT, numero TEXT, rue TEXT,complement TEXT, boite_postale TEXT, code_postal INT, ville TEXT, pays TEXT)',
			'CREATE TABLE IF NOT EXISTS personnes (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT)',
			'CREATE TABLE IF NOT EXISTS entreprises (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, adresse INT, FOREIGN KEY (adresse) REFERENCES adresses(id))',
			'CREATE TABLE IF NOT EXISTS factures (id INTEGER PRIMARY KEY AUTOINCREMENT, acheteur INT, adresse_acheteur INT, enseigne INT, prix_ht DOUBLE, prix_ttc DOUBLE, date_achat DATE, fichier LONGBLOB, FOREIGN KEY (acheteur) REFERENCES personnes(id), FOREIGN KEY (adresse_acheteur) REFERENCES adresses(id), FOREIGN KEY (enseigne) REFERENCES entreprises(id))',
			'CREATE TABLE IF NOT EXISTS fiches_paie (id INTEGER PRIMARY KEY AUTOINCREMENT, entreprise INT, employe INT, date DATE, revenu_brut DOUBLE, revenu_net DOUBLE, fichier LONGBLOB, FOREIGN KEY (entreprise) REFERENCES entreprises(id), FOREIGN KEY (employe) REFERENCES personnes(id) )',
			'CREATE TABLE IF NOT EXISTS modeles (id INTEGER PRIMARY KEY AUTOINCREMENT,nom_modele TEXT, type TEXT ,rectangle_x1_1 FLOAT, rectangle_x1_2 FLOAT, rectangley1_1 FLOAT, rectangley1_2 FLOAT, utilisation_rectangle1 TEXT,rectangle_x2_1 FLOAT, rectangle_x2_2 FLOAT, rectangley2_1 FLOAT, rectangley2_2 FLOAT, utilisation_rectangle2 TEXT,rectangle_x3_1 FLOAT, rectangle_x3_2 FLOAT, rectangley3_1 FLOAT, rectangley3_2 FLOAT, utilisation_rectangle3 TEXT,rectangle_x4_1 FLOAT, rectangle_x4_2 FLOAT, rectangley4_1 FLOAT, rectangley4_2 FLOAT, utilisation_rectangle4 TEXT,rectangle_x5_1 FLOAT, rectangle_x5_2 FLOAT, rectangley5_1 FLOAT, rectangley5_2 FLOAT, utilisation_rectangle5 TEXT,rectangle_x6_1 FLOAT, rectangle_x6_2 FLOAT, rectangley6_1 FLOAT, rectangley6_2 FLOAT, utilisation_rectangle6 TEXT,rectangle_x7_1 FLOAT, rectangle_x7_2 FLOAT, rectangley7_1 FLOAT, rectangley7_2 FLOAT, utilisation_rectangle7 TEXT,rectangle_x8_1 FLOAT, rectangle_x8_2 FLOAT, rectangley8_1 FLOAT, rectangley8_2 FLOAT, utilisation_rectangle8 TEXT,rectangle_x9_1 FLOAT, rectangle_x9_2 FLOAT, rectangley9_1 FLOAT, rectangley9_2 FLOAT, utilisation_rectangle9 TEXT,rectangle_x10_1 FLOAT, rectangle_x10_2 FLOAT, rectangley10_1 FLOAT, rectangley10_2 FLOAT, utilisation_rectangle10 TEXT,rectangle_x11_1 FLOAT, rectangle_x11_2 FLOAT, rectangley11_1 FLOAT, rectangley11_2 FLOAT, utilisation_rectangle11 TEXT,rectangle_x12_1 FLOAT, rectangle_x12_2 FLOAT, rectangley12_1 FLOAT, rectangley12_2 FLOAT, utilisation_rectangle12 TEXT,rectangle_x13_1 FLOAT, rectangle_x13_2 FLOAT, rectangley13_1 FLOAT, rectangley13_2 FLOAT, utilisation_rectangle13 TEXT,rectangle_x14_1 FLOAT, rectangle_x14_2 FLOAT, rectangley14_1 FLOAT, rectangley14_2 FLOAT, utilisation_rectangle14 TEXT)'
		]
		for instruction in instructions_sql:
			cursor.execute(instruction)
		self.connexion.commit()
		cursor.close()

	# <============ PARTIE ADRESSE ============>

	def ajouter_adresse(self, adresse: Adresse):
		"""
		TODO docstring
		:param adresse:
		:return:
		"""
		if self.est_dans_la_base_adresse(adresse.id):
			return self.avoir_adresse(adresse.id)
		cursor = self.connexion.cursor()
		cursor.execute(
			'INSERT INTO adresses (numero, rue, complement, boite_postale, code_postal, ville, pays) VALUES (?, ?, ?, ?, ?, ?,  ?, ?)',
			tuple(adresse.avoir_donnees().values()))
		self.connexion.commit()
		donnees = adresse.avoir_donnees()
		nouvelle_adresse = Adresse(donnees["numero_rue"], donnees["adresse"], donnees["complement"],
		                           donnees["boite_postale"], donnees["code_postal"], donnees["ville"], donnees["pays"],
		                           cursor.lastrowid)
		cursor.close()
		return nouvelle_adresse

	def avoir_adresse(self, id: int):
		"""
		TODO docstring
		:param id:
		:return:
		"""
		cursor = self.connexion.cursor()
		cursor.execute('SELECT * FROM adresses WHERE id = ?', (id,))
		resultat = cursor.fetchone()
		cursor.close()
		return Adresse(resultat[1], resultat[2], resultat[3], resultat[4], resultat[5], resultat[6], resultat[0])

	def est_dans_la_base_adresse(self, id: int) -> bool:
		"""
		TODO docstring
		"""
		cursor = self.connexion.cursor()
		cursor.execute('SELECT * FROM adresses WHERE id = ?', (id,))
		resultat = cursor.fetchone()
		cursor.close()
		return resultat is not None

	def avoir_identifiant_adresse(self, adresse: Adresse) -> int:
		"""
		TODO docstring
		"""
		adresses = self.avoir_toutes_les_adresses()
		for adresse_de_la_base in adresses:
			if adresse_de_la_base == adresse:
				return adresse_de_la_base.avoir_identifiant()
		return None

	def avoir_toutes_les_adresses(self):
		"""
		TODO docstring
		:return:
		"""
		cursor = self.connexion.cursor()
		cursor.execute('SELECT * FROM adresses')
		resultat = cursor.fetchall()
		adresses = []
		for adresse in resultat:
			adresse_classe = Adresse(adresse[1], adresse[2], adresse[3], adresse[4], adresse[5], adresse[6], adresse[0])
			adresses.append(adresse_classe)
		cursor.close()
		return adresses

	def modifier_adresse(self, id: int, nouvelle_adresse: Adresse) -> Adresse:
		"""
		TODO docstring
		"""
		if not self.est_dans_la_base_adresse(id):
			return None
		cursor = self.connexion.cursor()
		cursor.execute(
			"UPDATE adresses SET numero = ?, rue = ?, complement = ?, boite_postale = ?, code_postal = ?, ville = ? , pays = ? WHERE id = ?",
			tuple(nouvelle_adresse.avoir_donnees().values()) + (id,))
		self.connexion.commit()
		cursor.close()
		return self.avoir_adresse(id)

	def supprimer_adresse(self, id: int) -> None:
		"""
		TODO docstring
		"""
		if not self.est_dans_la_base_adresse(id):
			return None
		cursor = self.connexion.cursor()
		cursor.execute("DELETE FROM adresses WHERE id = ?", (id,))
		self.connexion.commit()
		cursor.close()

	# <============ PARTIE PERSONNE ============>

	def ajouter_personne(self, personne: Personne):
		"""
		TODO docstring
		:param adresse:
		:return:
		"""
		if self.est_dans_la_base_personne(personne.avoir_identifiant()):
			return self.avoir_personne(personne.avoir_identifiant())
		cursor = self.connexion.cursor()
		cursor.execute('INSERT INTO personnes (nom, prenom) VALUES (?, ?, ?, ?)',
						tuple(personne.avoir_donnees().values()))
		self.connexion.commit()
		donnees = personne.avoir_donnees()
		nouvelle_personne = Personne(donnees["nom"], donnees["prenom"], cursor.lastrowid)
		cursor.close()
		return nouvelle_personne

	def avoir_adresse(self, id: int):
		"""
		TODO docstring
		:param id:
		:return:
		"""
		cursor = self.connexion.cursor()
		cursor.execute('SELECT * FROM adresses WHERE id = ?', (id,))
		resultat = cursor.fetchone()
		cursor.close()
		return Adresse(resultat[1], resultat[2], resultat[3], resultat[4], resultat[5], resultat[6])

	def est_dans_la_base_personne(self, id: int) -> bool:
		"""
		TODO docstring
		"""
		cursor = self.connexion.cursor()
		cursor.execute('SELECT * FROM personnes WHERE id = ?', (id,))
		resultat = cursor.fetchone()
		cursor.close()
		return resultat is not None

	def avoir_identifiant_personne(self, personne: Personne) -> int:
		"""
		TODO docstring
		"""
		personnes = self.avoir_toutes_les_personnes()
		for personne_de_la_base in personnes:
			if personne_de_la_base == personne:
				return personne_de_la_base.avoir_identifiant()
		return None

	def avoir_toutes_les_personnes(self):
		"""
		TODO docstring
		:return:
		"""
		cursor = self.connexion.cursor()
		cursor.execute('SELECT * FROM personnes')
		resultat = cursor.fetchall()
		personnes = []
		for personne in resultat:
			personnes.append(Personne(personne[1], personne[2], personne[0]))
		cursor.close()
		return personnes

	def modifier_personne(self, id: int, nouvelle_personne: Personne) -> Personne:
		"""
		TODO docstring
		"""
		if not self.est_dans_la_base_personne(id):
			return None
		cursor = self.connexion.cursor()
		cursor.execute("UPDATE personnes SET nom = ?, prenom = ? WHERE id = ?",
		               tuple(nouvelle_personne.avoir_donnees().values()) + (id,))
		self.connexion.commit()
		cursor.close()
		return self.avoir_personne(id)

	def supprimer_personne(self, id: int) -> None:
		"""
		TODO docstring
		"""
		if not self.est_dans_la_base_personne(id):
			return None
		cursor = self.connexion.cursor()
		cursor.execute("DELETE FROM personnes WHERE id = ?", (id,))
		self.connexion.commit()
		cursor.close()

	# <============ PARTIE ENTREPRISE ============>

	def ajouter_entreprise(self, entreprise: Entreprise):
		"""
		TODO docstring
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

	def avoir_entreprise(self, id: int):
		curseur = self.connexion.cursor()
		curseur.execute("SELECT * FROM entreprises WHERE id = ?", (id,))
		resultat = curseur.fetchone()
		if resultat is None:
			return None
		adresse = self.avoir_adresse(resultat[2])
		return Entreprise(resultat[1], adresse, resultat[0])

	def avoir_identifiant_entreprise(self, entreprise: Entreprise) -> int:
		"""
		TODO docstring
		"""
		entreprises = self.avoir_toutes_les_entreprises()
		for entreprise_de_la_base in entreprises:
			if entreprise_de_la_base == entreprise:
				return entreprise_de_la_base.avoir_identifiant()
		return None

	def avoir_toutes_les_entreprises(self):
		"""
		TODO docstring
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
		TODO docstring
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
		TODO docstring
		"""
		curseur = self.connexion.cursor()
		if not self.est_dans_la_base_entreprise(id):
			return None
		curseur.execute("DELETE FROM entreprises WHERE id = ?", (id,))
		self.connexion.commit()
		curseur.close()

	def est_dans_la_base_entreprise(self, id: int) -> bool:
		"""
		TODO docstring
		"""
		curseur = self.connexion.cursor()
		curseur.execute("SELECT * FROM entreprises WHERE id = ?", (id,))
		resultat = curseur.fetchone()
		curseur.close()
		return resultat is not None

	# <============ PARTIE FACTURE ============>

	def ajouter_facture(self, facture: Facture):
		"""
		TODO docstring
		:param facture:
		:return:
		"""
		donnees = facture.avoir_donnees()
		donnees["adresse_acheteur"] = self.ajouter_adresse(donnees["adresse_acheteur"]).avoir_identifiant()
		donnees["enseigne"] = self.ajouter_entreprise(donnees["enseigne"]).avoir_identifiant()
		donnees["acheteur"] = self.ajouter_personne(donnees["acheteur"]).avoir_identifiant()
		cursor = self.connexion.cursor()
		cursor.execute(
			'INSERT INTO factures (acheteur, adresse_acheteur, enseigne, prix_ht, prix_ttc, date_achat, fichier) VALUES (?, ?, ?, ?, ?, ?, ?)',
			tuple(donnees.values()))
		self.connexion.commit()
		cursor.close()

	def avoir_facture(self, id: int) -> Facture:
		"""
		TODO docstring
		"""
		cursor = self.connexion.cursor()
		cursor.execute("SELECT * FROM factures WHERE id = ?", (id,))
		resultat = cursor.fetchone()
		if resultat is None:
			return None
		acheteur = self.avoir_personne(resultat[1])
		adresse_acheteur = self.avoir_adresse(resultat[2])
		enseigne = self.avoir_entreprise(resultat[3])
		return Facture(acheteur, adresse_acheteur, enseigne, resultat[4], resultat[5], resultat[6], resultat[7],
		               resultat[0])

	def avoir_identifiant_facture(self, facture: Facture) -> int:
		"""
		TODO docstring
		"""
		factures = self.avoir_toutes_les_factures()
		for facture_de_la_base in factures:
			if facture_de_la_base == facture:
				return facture_de_la_base.avoir_identifiant()
		return None

	def avoir_toutes_les_factures(self) -> list:
		"""
		TODO docstring
		"""
		cursor = self.connexion.cursor()
		cursor.execute("SELECT * FROM factures")
		resultat = cursor.fetchall()
		factures = list()
		for facture in resultat:
			acheteur = self.avoir_personne(facture[1])
			adresse_acheteur = self.avoir_adresse(facture[2])
			enseigne = self.avoir_entreprise(facture[3])
			facture_classe = Facture(acheteur, adresse_acheteur, enseigne, facture[4], facture[5], facture[6],
			                         facture[7], facture[0])
			factures.append(facture_classe)
		cursor.close()
		return factures

	def modifier_facture(self, id: int, nouvelle_facture: Facture) -> Facture:
		"""
		TODO docstring
		"""
		if not self.est_dans_la_base_facture(id):
			return None
		nouvelle_adresse_acheteur = self.ajouter_adresse(nouvelle_facture.avoir_adresse_acheteur())
		nouvelle_enseigne = self.ajouter_entreprise(nouvelle_facture.avoir_enseigne())
		nouvel_acheteur = self.ajouter_personne(nouvelle_facture.avoir_acheteur())
		cursor = self.connexion.cursor()
		cursor.execute(
			"UPDATE factures SET acheteur = ?, adresse_acheteur = ?, enseigne = ?, prix_ht = ?, prix_ttc = ?, date_achat = ?, fichier = ? WHERE id = ?",
			(nouvel_acheteur.avoir_identifiant(), nouvelle_adresse_acheteur.avoir_identifiant(),
			 nouvelle_enseigne.avoir_identifiant(), nouvelle_facture.avoir_prix_ht(), nouvelle_facture.avoir_prix_ttc(),
			 nouvelle_facture.avoir_date_achat(), nouvelle_facture.avoir_fichier(), id))
		self.connexion.commit()
		cursor.close()
		return self.avoir_facture(id)

	def supprimer_facture(self, id: int) -> None:
		"""
		TODO docstring
		"""
		if not self.est_dans_la_base_facture(id):
			return None

		cursor = self.connexion.cursor()
		cursor.execute("DELETE FROM factures WHERE id = ?", (id,))
		self.connexion.commit()
		cursor.close()

	def est_dans_la_base_facture(self, id: int) -> bool:
		"""
		TODO docstring
		"""
		cursor = self.connexion.cursor()
		cursor.execute("SELECT * FROM factures WHERE id = ?", (id,))
		resultat = cursor.fetchone()
		cursor.close()
		return resultat is not None

	# <============ PARTIE FICHE DE PAIE ============>

	def ajouter_fiche_paie(self, fiche_paie: Fiche_Paie):
		"""
		TODO docstring
		:param fiche_paie:
		:return:
		"""
		donnees = fiche_paie.avoir_donnees()
		entreprise_bdd = self.ajouter_entreprise(donnees["entreprise"])
		personne_bdd = self.ajouter_personne(donnees["employé"])
		cursor = self.connexion.cursor()
		cursor.execute(
			'INSERT INTO fiches_paie (entreprise, employe, date, revenu_brut, revenu_net, fichier) VALUES (?, ?, ?, ?, ?, ?)',
			tuple(donnees.values()))
		self.connexion.commit()
		cursor.close()

	def avoir_fiche_paie(self, id: int) -> Fiche_Paie:
		"""
		TODO docstring
		"""
		cursor = self.connexion.cursor()
		cursor.execute("SELECT * FROM fiches_paie WHERE id = ?", (id,))
		resultat = cursor.fetchone()
		cursor.close()
		if resultat is None:
			return None
		entreprise = self.avoir_entreprise(resultat[1])
		employe = self.avoir_personne(resultat[2])
		return Fiche_Paie(entreprise, employe, resultat[3], resultat[4], resultat[5], resultat[6], resultat[0])

	def avoir_identifiant_fiche_paie(self, fiche_paie: Fiche_Paie) -> int:
		"""
		TODO docstring
		"""
		fiches_paie = self.avoir_toutes_les_fiches_de_paie()
		for fiche_paie_de_la_base in fiches_paie:
			if fiche_paie_de_la_base == fiche_paie:
				return fiche_paie_de_la_base.avoir_identifiant()
		return None

	def avoir_toutes_les_fiches_de_paie(self):
		"""
		TODO docstring
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

	def modifier_fiche_paie(self, id: int, nouvelle_fiche_paie: Fiche_Paie) -> Fiche_Paie:
		"""
		TODO docstring
		"""
		if not self.est_dans_la_base_fiche_paie(id):
			return None
		donnees = nouvelle_fiche_paie.avoir_donnees()
		entreprise_bdd = self.modifier_entreprise(donnees["entreprise"])
		personne_bdd = self.modifier_personne(donnees["employé"])
		cursor = self.connexion.cursor()
		cursor.execute(
			'UPDATE fiches_paie SET entreprise = ?, employe = ?, date = ?, revenu_brut = ?, revenu_net = ?, fichier = ? WHERE id = ?',
			tuple(donnees.values()))
		self.connexion.commit()
		cursor.close()
		return self.avoir_fiche_paie(id)

	def supprimer_fiche_paie(self, id: int) -> None:
		"""
		TODO docstring
		"""
		if not self.est_dans_la_base_fiche_paie(id):
			return None
		cursor = self.connexion.cursor()
		cursor.execute("DELETE FROM fiches_paie WHERE id = ?", (id,))
		self.connexion.commit()
		cursor.close()

	def est_dans_la_base_fiche_paie(self, fiche_paie: Fiche_Paie):
		"""
		TODO docstring
		"""
		cursor = self.connexion.cursor()
		cursor.execute("SELECT * FROM fiches_paie WHERE id = ?", (fiche_paie.avoir_identifiant(),))
		resultat = cursor.fetchone()
		cursor.close()
		return resultat is not None
