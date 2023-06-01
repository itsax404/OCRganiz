from abc import ABC, abstractmethod

class Reconnaisseur(ABC):
    """Permet de faire des classes d'objets à partir des chaines
    de caractères fournis par l'OCR"""

    @abstractmethod
    def reconnaitre(self, chaine):
        pass