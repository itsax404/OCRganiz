from backend.images.reconnaisseurs.reconnaisseur import Reconnaisseur
import re

class Prix_Reconnaisseur(Reconnaisseur):
    """Reconnaisseur de prix"""

    def reconnaitre(self, chaine: str) -> float:
        """Reconnait un prix dans une chaine de caractères"""
        nettoyage = chaine.replace(",", " ").replace(".", " ")
        split = nettoyage.split(" ")
        for nombre in split:
            for chiffre in nombre:
                if (not chiffre.isdigit()) and (not chiffre in ",."):
                    raise ValueError("La chaîne n'est pas un prix valide")
        return float(chaine.replace(",", "."))

prix = Prix_Reconnaisseur()
