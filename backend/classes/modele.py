from .bases.entreprise import Entreprise
from .bases.personne import Personne
import datetime

class Modele:

    def __init__(self, donnees, nom: str) -> None:
        """
        TODO
        """
        self.attributs = []
        for i, donnee in enumerate(donnees):
            coordonnees = donnee["coordonnee"]
            type_donnee = donnee["type"]
            dictionnaire = {}
            setattr(self, f"rectangle_x{i+1}_1", coordonnees[0])
            dictionnaire[f"rectange_x{x+1}_1"] = cooordonnes[0]
            setattr(self, f"rectangle_x{i+1}_2", coordonnees[2])
            dictionnaire[f"rectange_x{x+1}_2"] = cooordonnes[2]
            setattr(self, f"rectangle_y{i+1}_1", coordonnees[1])
            dictionnaire[f"rectange_y{x+1}_1"] = cooordonnes[1]
            setattr(self, f"rectangle_y{i+1}_2", coordonnees[3])
            dictionnaire[f"rectange_y{x+1}_2"] = cooordonnes[3]
            setattr(self, f"type_{i+1}", type_donnee)
            dictionnaire[f"type_{id+1}"] = type_donnee
            self.attributs.append(dictionnaire)
    
        self.nom = nom

    def avoir_donnees(self):
        return self.attributs
        
     def avoir_nom(self):
     	return self.nom                                                              
                                                                                        
            