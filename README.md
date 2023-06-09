# Projet *OCRganiz*

## C'est quoi *OCRganiz* ?
Cela permet d'enregistrer des fichiers, telles que des factures, fiches de paie, en utilisant de l'OCR *(Opticial Recognization Character)* afin de pouvoir les trier.
## Prérequis
Dans un premier, l'installation des librairies est impérative :  
* [Tkinter](https://docs.python.org/3/library/tkinter.html)
* [Tesseract](https://github.com/UB-Mannheim/tesseract/)  
Une fois Tesseract correctement installé, il faut modifier le fichier .env en introduisant l'adresse du fichier .exe de tesseract dans le champ TESSERACT_DIR. 


## Comment utiliser *OCRganiz* 
Une fois le programme lancé, nous avons la fenêtre suivante :    
![image](https://github.com/itsax404/OCRganiz/assets/93085354/cedd6b58-0498-4320-b066-af8a7e66a2bb)  

Il s'agit de l'interface principale, cette fenêtre possède 4 fonctionnalités principales :     
* Gestion de la liste de fichiers (supprimer, ajouter, et tout sélectionner les fichiers).
* Visualisser le pdf, cette option permet de consulter le PDF ainsi qu'ajuster les paramètres pour l'OCR dont la definition des zones de reconnaissances
* Définir les types d'un fichier, c'est-à-dire définir si le fichier est une facture ou une fiche de paie ainsi que le modèle correspondant
* Insérer les données récupérées par l'algorithme OCR dans la base de données
![image](https://github.com/itsax404/OCRganiz/assets/93085354/611760f8-be8b-4add-b4ef-b4123fd2c5a5)  

Cette interface permet des créer nos propres modèles pour un type de fichier (facture, fiche de paie) :
* le bouton "test" permet d'afficher le résultat de l'OCR ainsi l'utilisateur peut vérifier la zone sélectionnée
* L'option "Debug" affiche toutes les zones enregistrées en bleu
* L'option deroulant gère le choix du type de fichier
* Le bouton "Enregistrer zone de détection" sauvegarde la zone définie et la sélection dans le tableau des valeurs importantes
* "Enregistrer modèle" insère les données des zones dans la base de données

[video de présentation](https://www.dailymotion.com/video/x8lwtsi)
## Annexes
Le [Trello](https://trello.com/invite/b/updv2xap/ATTId970c379082223d06ecea2d2e0a76bb207D679C6/projet-programmation)
