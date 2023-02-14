from PIL import Image
from urllib.request import urlopen
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd

imageFile = fd.askopenfilename(filetypes=(('Image File', '*.png'), ("Jpg file", "*.jpg"), ("Bmp file", "*.bmp")))
secretImageFile = fd.askopenfilename(filetypes=(('Image File', '*.png'), ("Jpg file", "*.jpg"), ("Bmp file", "*.bmp")))

imageURL = "https://www.radiofrance.fr/s3/cruiser-production/2022/06/5f6ac5ab-37d9-4ca6-8f79-3694fcfec071/560x315_paysage-monet.jpg"
secretImageURL = r"https://www.tictactrip.eu/blog/wp-content/uploads/2020/07/Format-Blog-bannie%CC%80re-article-26-1-1160x652.png"

imageSRC = "Capture d'écran_20230204_221251.png"
secretImageSRC = "Capture d'écran_20230205_211753.png"

image = Image.open(imageFile)
image = image.convert("RGB")

imageTk = tk.PhotoImage(image)

imageSecret = Image.open(secretImageFile)
maxSize = (image.width, image.height)
imageSecret = imageSecret.resize(maxSize)
imageSecret = imageSecret.convert("RGB")


window = tk.Tk()
window.title("Stéganographe")

frame = tk.Frame(window)
frame.pack()

image1 = tk.Label(frame, image=imageTk)
image1.pack()

textLoading = tk.Label(frame, text='Patientez...', font=('Calibri', 12))
textLoading.pack()

progressbar = ttk.Progressbar(frame, length=100, mode='determinate')
progressbar.pack()


    # On encode
def modifImage():
    for i in range(image.width):
        if round(i/image.width*100) - round(i-1/image.width*100)!=0:
            progressbar["value"] = round(i/image.width*100)
            window.update() 
        for j in range(image.height):
            pixel = image.getpixel((i,j))
            pixelSecret = imageSecret.getpixel((i,j))

            newPixel = list()

            for k in range(len(pixel)):
                colorBin = bin(pixel[k])
                secretColorBin = bin(pixelSecret[k])
                finalColorBin = ''
                while len(colorBin) <= 6:
                    colorBin += '0'
                for l in range(len(colorBin)):
                    if l<=7:
                        finalColorBin += colorBin[l]
                    if l>=8 and len(secretColorBin)>l-6:
                        finalColorBin += secretColorBin[l-6]

                finalColorBin = int(finalColorBin, 2)
                newPixel.append(finalColorBin)

            # print(f"{pixel} -> {newPixel}")
            newPixel = tuple(newPixel)

            image.putpixel((i,j), newPixel)
    image.show()

    # On décode

    for i in range(image.width):
        for j in range(image.height):
            pixel = image.getpixel((i, j))

            newPixel = list()

            for k in range(len(pixel)):
                secretColorBin = bin(pixel[k])
                finalColorBin = ""

                for l in range(len(secretColorBin)):
                    if l>=len(secretColorBin) - 4  and l>1:
                        finalColorBin += secretColorBin[l]

                while len(finalColorBin)<8:
                    finalColorBin+='0'

                finalColorBin = int(finalColorBin, 2)
                newPixel.append(finalColorBin)

            newPixel = tuple(newPixel)

            image.putpixel((i,j), newPixel)
    image.show()

modifImage()
window.mainloop()
