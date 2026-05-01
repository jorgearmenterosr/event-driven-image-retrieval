from PIL import Image

img = Image.open("image1.png")

print("Size:", img.size)
print("Mode:", img.mode)