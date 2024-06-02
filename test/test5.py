from PIL import Image, ImageDraw

# Dimensions de l'image
width, height = 20, 120  # Plus courte, moins haute

# Création d'une nouvelle image RGBA (transparence)
img = Image.new('RGBA', (width, height), (0, 0, 0, 0))

# Dessin du rectangle arrondi gris foncé avec ImageDraw
draw = ImageDraw.Draw(img)
border_radius = 10  # Rayon pour des coins plus arrondis
draw.rounded_rectangle([(3, 3), (width - 3, height - 3)], fill=(50, 50, 50, 230), outline=None, radius=border_radius)

# Sauvegarde de l'image
img.save('colonne_courte_foncee.png')

# Affichage de l'image générée
img.show()



