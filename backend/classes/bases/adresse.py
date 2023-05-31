class Adresse:

	def __init__(self, numero_rue: str, nom_rue: str, code_postal: int, ville: str, pays: str, complement=None, boite_postale=None, id: int = -1):
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
		self.complement = complement
		self.boite_postale= boite_postale
		self.ville = ville
		self.pays = pays
		self.id = id

	def __str__(self):
		return f"{self.avoir_donnees()}"

	def __eq__(self, other):
		return( self.numero_rue.lower() == other.numero_rue.lower()) and (self.nom_rue.lower() == other.nom_rue.lower()) and (self.code_postal == other.code_postal) and (self.ville == other.ville)

	def avoir_identifiant(self):
		return self.id

	def avoir_donnees(self):
		return {"numero_rue": self.numero_rue, "adresse": self.nom_rue, "complement": self.complement,
		        "boite_postale": self.boite_postale,
		        "code_postal": self.code_postal, "ville": self.ville, "pays": self.pays}
