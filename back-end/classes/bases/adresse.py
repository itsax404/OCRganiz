class Adresse:

	def __init__(self, numero_rue: int, nom_rue: str, code_postal: int, ville: str, pays: str, residence: str = None,
	             appartement: str = None, batiment: str = None, id: int = -1):
		"""
		TODO docstring
		:param numero_rue:
		:param adresse:
		:param code_postal:
		:param ville:
		:param region:
		:param pays:
		"""
		self.numero_rue = numero_rue
		self.nom_rue = nom_rue
		self.code_postal = code_postal
		self.ville = ville
		self.residence = residence
		self.appartement = appartement
		self.batiment = batiment
		self.pays = pays
		self.id = id

	def __str__(self):
		return f"{self.avoir_donnees()}"

	def __eq__(self, other):
		return (self.nom_rue.lower() == other.nom_rue.lower()) and (self.appartement == other.appartement) and (
				self.batiment == other.batiment) and (self.residence == other.residence) and (
				self.numero_rue == other.numero_rue) and (self.ville.lower() == other.ville.lower()) and (
				self.code_postal == self.code_postal)

	def avoir_identifiant(self):
		return self.id

	def avoir_donnees(self):
		return {"numero_rue": self.numero_rue, "adresse": self.nom_rue, "residence": self.residence,
		        "appartement": self.appartement, "batiment": self.batiment,
		        "code_postal": self.code_postal, "ville": self.ville, "pays": self.pays}
