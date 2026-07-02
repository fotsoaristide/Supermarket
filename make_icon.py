from PIL import Image

img = Image.open("astro_logo.jpeg")

img.save("astro.ico", format="ICO", sizes=[(256, 256)])
print("ICO créé avec succès")