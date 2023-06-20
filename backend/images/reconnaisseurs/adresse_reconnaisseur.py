from .reconnaisseur import Reconnaisseur

from backend.classes.bases.adresse import Adresse
class Adresse_Reconnaisseur(Reconnaisseur):

	def __init__(self):
		self.complement = ""
		self.numero = ""
		self.adresse = ""
		self.boite_postale = ""
		self.code_postal = 0
		self.ville = ""
		self.pays = "France"

	def est_un_nombre(self, chaine):
		for lettre in chaine:
			if lettre not in "0123456789":
				return False
		return True
	def avoir_cp_ville(self, chaine):
		nb_digits = 0
		debut = -1
		fin = -1
		cp = "-1"
		mots = [mot for mot in list(chaine.split(" ")) if mot != ""]
		for i, mot in enumerate(mots):
			for lettre in mot:
				if self.est_un_nombre(lettre):
					nb_digits += 1
				if nb_digits == 5:
					cp = mots[i-1]
		if cp == "-1" or (cp == "BP"):
			return None
		else:
			mots_restants = [mot for mot in mots if mot != ""]
			for mot in mots_restants:
				if mot != cp:
					return (cp, mot)
	def avoir_bp(self, chaine):
		bp = False
		numero = -1
		mots_restants = [mot.lower() for mot in chaine.split(" ") if mot != ""]
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
					numero = mot
		if not bp or numero == "-1":
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
				if i != 0:
					numero = "-1"
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
		for i, valeur in enumerate(liste_valeurs):
			if self.avoir_cp_ville(valeur) is not None:
				self.code_postal, self.ville = self.avoir_cp_ville(valeur)
			elif self.avoir_bp(valeur) is not None:
				self.boite_postale = " ".join(list(self.avoir_bp(valeur)))
			elif self.avoir_numero_adresse(valeur) is not None:
				self.numero, self.adresse = self.avoir_numero_adresse(valeur)
			else:
				self.complement = valeur
    
	def avoir(self):
		return Adresse(self.numero, self.adresse, self.code_postal, self.ville, self.pays, self.complement, self.boite_postale)