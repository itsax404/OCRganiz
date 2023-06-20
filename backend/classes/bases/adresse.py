class Adresse:

	def __init__(self, numero_rue: str = None, nom_rue: str = None, code_postal: str = None, ville: str = None, pays: str = None, complement=None,
	             boite_postale=None, id: int = -1) -> None:
		"""
		Permet créer un objet `Adresse` qui contient les informations d'une adresse postale.
		:param numero_rue: Le numéro de la rue (avec 'bis', 'ter', etc.)
		:type numero_rue: str
		:param nom_rue: Le nom de la rue
		:type nom_rue: str
		:param code_postal: Le code postal de la ville
		:type code_postal: int
		:param ville: Le nom de la ville
		:type ville: str
		:param pays: Le nom du pays
		:type pays: str
		:param complement: Le complément d'adresse (facultatif)
		:type complement: str
		:param boite_postale: Le numéro de boîte postale (facultatif)
		:type boite_postale: str
		:param id: L'identifiant de l'adresse dans la base de données
		:type id: int
		"""
		self.numero_rue = numero_rue
		self.nom_rue = nom_rue
		self.code_postal = code_postal
		self.complement = complement
		self.boite_postale = boite_postale
		self.ville = ville
		self.pays = pays
		self.id = id

	def __str__(self) -> str:
		"""
		Permet de renvoyer les données de l'adresse afin de les afficher.
		:return: Les données de l'adresse en format str
		:rtype: str
		"""
		return f"{self.avoir_donnees()}"

	def __eq__(self, other) -> bool:
		"""
		Permet de comparer deux adresses.
		:param other: L'autre adresse
		:type other: Adresse
		:return: Si les deux adresses sont identiques
		:rtype: bool
		"""
		return (self.numero_rue.lower() == other.numero_rue.lower()) and (
					self.nom_rue.lower() == other.nom_rue.lower()) and (self.code_postal == other.code_postal) and (
					self.ville == other.ville)

	def avoir_identifiant(self) -> int:
		"""
		Permet d'avoir l'identifiant de l'adresse.
		:return: l'identifiant de l'adresse
		:rtype: int
		"""
		return self.id

	def avoir_donnees(self):
		"""
		Permet d'avoir les données de l'adresse.
		:return: les données de l'adresse
		:rtype: dict
		"""
		return {"numero_rue": self.numero_rue, "adresse": self.nom_rue, "complement": self.complement,
		        "boite_postale": self.boite_postale,
		        "code_postal": self.code_postal, "ville": self.ville, "pays": self.pays}

	def avoir_numero(self):
		return self.numero_rue

	def avoir_rue(self):
		return self.nom_rue

	def avoir_boite_postale(self):
		return self.boite_postale

	def avoir_code_postal(self):
		return self.code_postal

	def avoir_ville(self):
		return self.ville

	def avoir_pays(self):
		return self.pays

	def modifier_numero(self, numero_rue):
		self.numero_rue = numero_rue

	def modifier_rue(self, nom_rue):
		self.nom_rue = nom_rue

	def modifier_boite_postale(self, boite_postale):
		self.boite_postale = boite_postale

	def modifier_code_postal(self, code_postal):
		self.code_postal = code_postal

	def modifier_complement(self, complement):
		self.complement = complement
	def modifier_ville(self, ville):
		self.ville = ville

	def modifier_pays(self, pays):
		self.pays = pays