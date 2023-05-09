class Adresse:

	def __init__(self, numero_rue: int, nom_rue: str, code_postal: int, ville: str, region: str, pays: str):
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
		self.region = region
		self.pays = pays

	def __str__(self):
		return f"{self.avoir_donnees()}"

	def __eq__(self, other):
		return (self.nom_rue.lower() == other.nom_rue.lower()) and (self.numero_rue == other.numero_rue) and (self.ville == other.ville) and (self.code_postal == self.code_postal)

	def avoir_donnees(self):
		return {"numero_rue": self.numero_rue, "adresse": self.nom_rue, "code_postal": self.code_postal,
		        "ville": self.ville, "region": self.region, "pays": self.pays}
