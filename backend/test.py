from classes.modele import Modele
from database import Database

db = Database()
modeles = db.avoir_tous_les_modeles()
print(modeles)
print(modeles[0].avoir_donnees())
