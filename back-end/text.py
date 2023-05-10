from classes.bases.adresse import Adresse
from classes.bases.entreprise import Entreprise
from database import Database

db = Database()

a = Adresse(883, "Route de Cairanne", 26790, "Tulette", "Auvergne-Rhône-Alpes", "France")

db.ajouter_adresse(a)

e = Entreprise("Cave Davin", a)
db.ajouter_entreprise(e)
