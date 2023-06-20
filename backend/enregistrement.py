import fitz

from backend.classes.bases import Personne, Entreprise, Adresse


def convertir_fichier(fichier):
    with open(fichier, 'rb') as file:
        donnees_binaires = file.read()
    return donnees_binaires


def enregistrer(liste_fichiers, database, image_processor, path) -> None:
    """
    Permet d'enregistrer plusieurs fichiers dans la base de données
        {fichier: "", modele: ""}
    :param liste_fichiers: liste des fichiers à enregistrer
    :type liste_fichiers: list[dict]
    :param type: type de fichier à enregistrer
    :type type: str
    :param modele: modèle du fichier à enregistrer
    :type modele: str
    :param database: base de données
    :type database: Database
    :return: None
    :rtype: None
    """
    for data in liste_fichiers:
        fichier_path = data["fichier"]
        modele_str = data["modele"]
        modele = database.avoir_modele(modele_str)
        pdf = fitz.open(fichier_path)
        images = [page.get_pixmap(dpi=300) for page in pdf.pages()]
        fichier = convertir_fichier(fichier_path)
        liste_coordonnées = list()
        for i, coords in enumerate(modele.avoir_donnees()):
            dictionnaire_coordonnees = {}
            page = coords[f"page_rectangle{i + 1}"]
            utilisation = coords[f"utilisation_rectangle{i + 1}"]
            coordonnees = tuple((coords[f"rectangle_x{i+1}_1"], coords[f"rectangle_x{i+1}_2"], coords[f"rectangle_y{i+1}_1"], coords[f"rectangle_y{i+1}_2"]))
            dictionnaire_coordonnees["coordonnées"] = coordonnees
            dictionnaire_coordonnees["type"] = utilisation
            dictionnaire_coordonnees["page"] = page
            liste_coordonnées.append(dictionnaire_coordonnees)
        objet = image_processor.reconnaitre(images, liste_coordonnées, modele.avoir_type(), path)
        objet.modifier_fichier(fichier)
        if modele.type == "facture":
            database.ajouter_facture(objet)
        elif modele.type == "fiche de paie":
            database.ajouter_fiche_paie(objet)
