from classes.bases.adresse import Adresse
from classes.bases.entreprise import Entreprise
from classes.bases.personne import Personne
from database import Database
from classes.fiche_paie import Fiche_Paie
from classes.facture import Facture
import datetime

db = Database()
a = """
a = Adresse(883, "Route de Cairanne", 26790, "Tulette", "Auvergne-Rhône-Alpes", "France")

db.ajouter_adresse(a)

e = Entreprise("Cave Davin", a)
db.ajouter_entreprise(e)

p = Personne("Quentin", "DAVIN")

db.ajouter_personne(p)

db.ajouter_facture(Facture(p, Adresse(14, "avenue du Stand", 21000, "Dijon", "Bourgogne-Franche-Comté", "France"), e, 120.0, 144.0, datetime.date.today(), bytes("Salut", "utf-8")))

p2 = Personne("Thomas", "GIROUD")
fp = Fiche_Paie(e, p2, datetime.date.today(), 5000.0, 3750.0, bytes("C'est un moins de 10", "utf-8"))
db.ajouter_fiche_paie(fp)"""

db.supprimer_facture(Facture(Personne("Quentin", "DAVIN"), Adresse(14, "avenue du Stand", 21000, "Dijon", "Bourgogne-Franche-Comté", "France", 1), Entreprise("Cave Davin", Adresse(883, "route de Cairanne", 26790, "Tulette", "Auvernge-Rhône-Alpes", "France", 1)), 120.0, 144.0, datetime.date.today(), bytes("Salut", "utf-8"), 3))