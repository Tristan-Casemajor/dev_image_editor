from PIL import Image, ImageDraw, ImageFont


im = Image.open("color_image.jpg")

out = im.rotate(90)

out.save("test_replace4.png")




# Charger l'image
image_path = "test_replace2.png"
image = Image.open(image_path)

# Créer un objet ImageDraw pour dessiner sur l'image
draw = ImageDraw.Draw(image)

# Spécifier le texte à ajouter
texte = "qqqqqqqqqqqqqqqqqq"

# Spécifier la police et la taille du texte
font = ImageFont.truetype("C:\\Users\\Trist\\PycharmProjects\\dev_image_edit\\fonts\\arial_unicode_ms.ttf", 26)  # Spécifiez le chemin de votre police et la taille souhaitée

# Spécifier la couleur du texte (en RGB)
couleur_texte = (255, 255, 255)  # Blanc

# Spécifier les coordonnées où le texte sera placé
position_texte = (100, 150)

# Dessiner le texte sur l'image
draw.text(position_texte, texte, fill=couleur_texte, font=font)

# Enregistrer l'image modifiée
image.save("test_replace2.png")

# Afficher l'image modifiée
image.show()





