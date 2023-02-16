from PIL import Image
from urllib.request import urlopen

image = Image.open(urlopen('https://media.lesechos.com/api/v1/images/view/6203b47f8fe56f43fc4f5a66/1280x720/070889361477-web-tete.jpg'))

image = image.convert("RGB")

for i in range(image.width):
    for j in range(image.height):
        pixel = image.getpixel((i, j))

        newpixel = list()

        for k in range(len(pixel)):
            colorBin = bin(pixel[k])
            newColorBin = '0b'

            for l in range(1, len(colorBin) - 2):
                newColorBin += colorBin[-l]

            while len(newColorBin)<10:
                newColorBin += '0'
            
            newColorBin = int(newColorBin, 2)
            newpixel.append(newColorBin)

        newpixel = tuple(newpixel)

        image.putpixel((i,j), newpixel)

image.show()