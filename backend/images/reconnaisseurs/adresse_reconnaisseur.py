from reconnaisseur import Reconnaisseur
import re

class Adresse_Reconnaisseur(Reconnaisseur):

	def __init__(self):
		self.complement = ""
		self.numero = ""
		self.adresse = ""
		self.boite_postale = ""
		self.code_postal = 0
		self.ville = ""
		self.pays = "France"

	def avoir_cp_ville(self, chaine):
		nb_digits = 0
		debut = -1
		fin = -1
		cp = "-1"
		mots = [mot for mot in list(chaine.split(" ")) if mot != ""]
		for i, mot in enumerate(mots):
			for lettre in mot:
				if lettre in "0123456789":
					nb_digits += 1
				if nb_digits == 5:
					cp = mots[i-1]
		if cp == "-1":
			return None
		else:
			mots_restants = [mot for mot in mots if mot != ""]
			for mot in mots_restants:
				if mot != cp:
					return (cp, mot)
	def avoir_bp(self, chaine):
		bp = False
		numero = -1
		mots_restants = [mot for mot in chaine if mot != ""]
		for mot in mots_restants:
			if mot.lower() == "bp":
				bp = True
			else:
				test = list()
				for lettre in mot:
					if lettre in "0123456789":
						test.append(True)
					else:
						test.append(False)
				if bp and all(test):
					numero = int(mot)
		if not bp or numero == -1:
			return None
		return ("BP", numero)

	def avoir_numero_adresse(self, chaine):
		if self.avoir_cp_ville(chaine) is not None:
			return None
		if self.avoir_bp(chaine) is not None:
			return None
		numero = "-1"
		adresse = ""
		mots_restants = [mot for mot in chaine.split(" ") if mot != ""]
		mots_restants_min = [mot.lower() for mot in mots_restants]
		cardinaux_multiplicatifs = ["bis", "ter", "quater"]
		cardinal_multiplicatif = ""
		for cardinal in cardinaux_multiplicatifs:
			if cardinal in mots_restants:
				cardinal_multiplicatif = cardinal
		for i, mot in enumerate(mots_restants_min):
			test = list()
			for lettre in mot: 
				if lettre in "0123456789":
					test.append(True)	
				else:
					test.append(False)
			if all(test):
				numero = mots_restants[i]
			elif mot == cardinal_multiplicatif:
				pass
			else:
				adresse += mots_restants[i]
				if i != len(mots_restants_min) - 1:
					adresse += " " 
		
		if numero == "-1":
			return None
		numero += f" {cardinal_multiplicatif}" if cardinal_multiplicatif != "" else ""
		return (numero , adresse)
	
	def reconnaitre(self, chaine):
		liste_valeurs = chaine.split("\n")
		print(liste_valeurs)
		for i, valeur in enumerate(liste_valeurs):
			if self.avoir_cp_ville(valeur) is not None:
				print(f"a - {valeur}")
				self.code_postal, self.ville = self.avoir_cp_ville(valeur)
			elif self.avoir_bp(valeur) is not None:
				print(f"b - {valeur}")
				self.boite_postale = " ".join(list(self.avoir_bp(valeur)))
			elif self.avoir_numero_adresse(valeur) is not None:
				print(f"c - {valeur}")
				self.numero, self.adresse = self.avoir_numero_adresse(valeur)
			else:
				print(f"d - {valeur}")
				self.complement = valeur
    
	def avoir(self):
		return {"numéro": self.numero, "complément": self.complement, "adresse": self.adresse,"boite_postale": self.boite_postale, "code_postal": self.code_postal, "ville": self.ville, "pays": self.pays}

ap = Adresse_Reconnaisseur()
adresse1 = " 61 rue Reine Elisabeth \n 06500 Menton"
ap.reconnaitre(adresse1)
print(ap.avoir())
adresse2 = "458 bis avenue du Stand \n 26000 Valence"
ap.reconnaitre(adresse2) 
print(ap.avoir())

adresse3 = "Résidences Le Chemisier Batiment 7 Appart 535 \n56 avenue Marie Curie\n21000 Dijon"
ap.reconnaitre(adresse3)
print(ap.avoir())