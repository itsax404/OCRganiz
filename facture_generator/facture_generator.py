from faker import Faker
import os
from PIL import Image, ImageFont, ImageDraw
import random

def avoir_numero_adresse(chaine):
	numero = "-1"
	adresse = ""
	mots_restants = [mot for mot in chaine.split(" ") if mot != ""]
	mots_restants_min = [mot.lower() for mot in mots_restants]
	cardinaux_multiplicatifs = ["bis", "ter", "quater"]
	cardinal_multiplicatif = ""
	for cardinal in cardinaux_multiplicatifs:
		if cardinal in mots_restants:
			cardinal_multiplicatif = cardinal
	for i, mot in enumerate(mots_restants_min):
		test = list()
		for lettre in mot:
			if lettre in "0123456789":
				test.append(True)
			else:
				test.append(False)
		if all(test):
			numero = mots_restants[i]
			if i != 0:
				numero = "-1"
		elif mot == cardinal_multiplicatif:
			pass
		else:
			adresse += mots_restants[i]
			if i != len(mots_restants_min) - 1:
				adresse += " "

	if numero == "-1":
		return None
	numero += f" {cardinal_multiplicatif}" if cardinal_multiplicatif != "" else ""
	return (numero, adresse)

def avoir_adresse():
	adresse = fake.address().replace(",", "")
	if avoir_numero_adresse(adresse) is not None:
		return adresse
	else:
		return avoir_adresse()

fake = Faker(["fr_FR"])
os.environ["INVOICE_LANG"] = "fr"
def generate_invoice():
	template = Image.open("template.jpg")
	template.convert("RGBA")

	font = ImageFont.truetype("lgc.ttf", 20)
	font_bold = ImageFont.truetype("lgc_bold.ttf", 20)

	logo = Image.open("img.png")
	logo.convert("RGBA")
	logo = logo.resize( [int(0.25 * s) for s in logo.size] )

	template.paste(logo, (90, 80), logo)

	draw = ImageDraw.Draw(template)



	entreprise = fake.company().replace("\n", "")
	draw.text((90, 251), entreprise, font=font_bold, fill=(0, 0, 0))
	entreprise_adresse, entreprise_ville  = avoir_adresse().split("\n")
	draw.text((90, 281), entreprise_adresse, font=font, fill=(0, 0, 0))
	draw.text((90, 313), entreprise_ville, font=font, fill=(0, 0, 0))
	draw.text((90, 341), fake.phone_number(), font=font, fill=(0, 0, 0))
	draw.text((90, 372), fake.email(), font=font, fill=(0, 0, 0))



	sex = random.randint(0, 1)

	client_name = ""

	if sex == 0:
		prefix = random.choice(["Mme.", "Madame"])
		client_name += prefix
		client_name += " "
		client_name += fake.name_female()
	else:
		prefix = random.choice(["Monsieur", "M."])
		client_name += prefix
		client_name += " "
		client_name += fake.name_male()

	draw.text((780, 402), client_name, font=font_bold, fill=(0, 0, 0))
	client_adresse, client_ville = avoir_adresse().split("\n")
	draw.text((780, 433), client_adresse, font=font, fill=(0, 0, 0))
	draw.text((780, 462), client_ville, font=font, fill=(0, 0, 0))
	draw.text((780, 492), fake.phone_number(), font=font, fill=(0, 0, 0))
	draw.text((780, 522), fake.email(), font=font, fill=(0, 0, 0))

	numero_facture = random.randint(1, 9999)
	draw.text((828, 190), f"Facture n°{numero_facture}", font=font_bold, fill=(255, 255, 255))

	date = fake.date().replace("-", "/")
	elements_date = date.split("/")
	date = f"{elements_date[2]}/{elements_date[1]}/{elements_date[0]}"
	draw.text((827, 157), f"Date : {date}", font=font_bold, fill=(255, 255, 255))

	mots_aleatoires = ["Baignoire", "Coffre","Yacht", "Camion", "Rênes", "Sauce", "Table", "Cabine", "Cadre","Cartes", "Costume", "Foulard", "Portefeuille"]
	mots_choisis = random.sample(mots_aleatoires, 7)

	montant_ht = 0
	objects = list()
	for i in range(7):
		description = mots_choisis[i]
		unité = "1 p"
		quantite = random.randint(1, 20)
		unite_ht = random.randint(1, 100)
		tva = "20 %"
		prix_ht = quantite * unite_ht
		montant_ht += prix_ht
		dictionnaire = {"description": description, "unité": unité, "quantité": quantite, "unité_ht": unite_ht, "tva": tva, "prix_ht": prix_ht}
		objects.append(dictionnaire)

	remise_ht = 0
	montant_ttc = montant_ht * 1.2
	montant_payé = 0
	reste_a_payer = montant_ttc

	coordonnées_description = [(83, 670), (83, 707), (83, 745), (83, 782), (83, 820), (83, 857), (83, 895)]
	coordonnées_unité = [(464, 670), (464, 707), (464, 745), (464, 782), (464, 820), (464, 857), (464, 895)]
	coordonnées_quantité = [(539, 670), (539, 707), (539, 745), (539, 782), (539, 820), (539, 857), (539, 895)]
	coordonnées_unité_ht = [(668, 670), (668, 707), (668, 745), (668, 782), (668, 820), (668, 857), (668, 895)]
	coordonnées_tva = [(842, 670), (842, 707), (842, 745), (842, 782), (842, 820), (842, 857), (842, 895)]
	coordonnées_prix_ht = [(924, 670), (924, 707), (924, 745), (924, 782), (924, 820), (924, 857), (924, 895)]



	for i in range(7):
		donnees = objects[i]
		x, y = coordonnées_description[i]
		draw.text((x+5, y+8), donnees["description"], font=font, fill=(0, 0, 0))
		x, y = coordonnées_unité[i]
		draw.text((x+5, y+8), donnees["unité"], font=font, fill=(0, 0, 0))
		x, y = coordonnées_quantité[i]
		draw.text((x+5, y+8), str(donnees["quantité"]) , font=font, fill=(0, 0, 0))
		x, y = coordonnées_unité_ht[i]
		draw.text((x+5, y+8), f"""{donnees["unité_ht"]} €""", font=font, fill=(0, 0, 0))
		x, y = coordonnées_tva[i]
		draw.text((x+5, y+8), donnees["tva"], font=font, fill=(0, 0, 0))
		x, y = coordonnées_prix_ht[i]
		draw.text((x+5, y+8),f"""{donnees["prix_ht"]} €""", font=font, fill=(0, 0, 0))

	draw.text((1010, 950 + 10), f"""{montant_ht} €""", font=font, fill=(0, 0, 0))
	draw.text((1010, 994 + 10), f"""{remise_ht} €""", font=font, fill=(0, 0, 0))
	draw.text((1010, 1034 + 12), f"""{montant_ht} €""", font=font, fill=(0, 0, 0))
	draw.text((1010, 1074 + 15), f"""{round(montant_ttc - montant_ht, 3)} €""", font=font, fill=(0, 0, 0))
	draw.text((1010, 1114 + 22), f"""{round(montant_ttc, 3)} €""", font=font_bold, fill=(0, 0, 0))
	draw.text((1010, 1154 + 27), f"""{montant_payé} €""", font=font, fill=(0, 0, 0))
	draw.text((1010, 1194 + 27), f"""{round(reste_a_payer, 3)} €""", font=font, fill=(0, 0, 0))

	font_warning = ImageFont.truetype("lgc_bold.ttf", 30)
	draw.text((200, 1671), "Cette facture est fausse. Toute correspondence est fortuite.", font=font_warning, fill=(255, 0, 0))
	return template

for i in range(100):
	print(f"Facture n°{i} en génération")
	template = generate_invoice()
	template.save(f".\\factures\\facture_{i}.png")
	print(f"Facture n°{i} générée")