from PIL import Image, ImageDraw

# Charger l'image
image = Image.open("icone_support_logiciel.png")

# Créer un masque de la même taille que l'image avec une couleur spécifique
overlay_color = (0, 255, 0, 128)  # Couleur avec une opacité réduite (ici, vert semi-transparent)
overlay = Image.new('RGBA', image.size, overlay_color)

# Fusionner l'image et le masque
result = Image.alpha_composite(image.convert('RGBA'), overlay)

result.save("image_overlay.png")