from PIL import Image, ImageTk
from urllib.request import urlopen
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import time

"""imageFile = fd.askopenfile(filetypes=(('Png File', '*.png'), ("Jpg file", "*.jpg"), ("Bmp file", "*.bmp")))
secretImageFile = fd.askopenfile(filetypes=(('Png File', '*.png'), ("Jpg file", "*.jpg"), ("Bmp file", "*.bmp")))"""

imageURL = "https://www.radiofrance.fr/s3/cruiser-production/2022/06/5f6ac5ab-37d9-4ca6-8f79-3694fcfec071/560x315_paysage-monet.jpg"
secretImageURL = r"https://www.tictactrip.eu/blog/wp-content/uploads/2020/07/Format-Blog-bannie%CC%80re-article-26-1-1160x652.png"

image = Image.open(urlopen(imageURL))
image = image.convert("RGB")


imageSecret = Image.open(urlopen(secretImageURL))
maxSize = (image.width, image.height)
imageSecret = imageSecret.resize(maxSize)
imageSecret = imageSecret.convert("RGB")


window = tk.Tk()
window.title("Stéganographe")

frame = tk.Frame(window)
frame.pack()

imageTk = ImageTk.PhotoImage(image)
secretImageTk = ImageTk.PhotoImage(imageSecret)

frameImages = tk.Frame(frame)
frameImages.pack()

image1 = tk.Label(frameImages, image=imageTk)
image1.pack(side = 'left')

textPlus = tk.Label(frameImages, text="+", font=('Calbri', 25))
textPlus.pack(side= 'left')

image2 = tk.Label(frameImages, image = secretImageTk)
image2.pack(side = 'left')

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
    imageFinalTk = ImageTk.PhotoImage(image)
    progressbar.pack_forget()
    textLoading.pack_forget()
    textFinal = tk.Label(frameImages, text='=>', font=("Calibri", 15))
    imageFinal = tk.Label(frameImages, image=imageFinalTk)
    textFinal.pack(side = "left")
    imageFinal.pack(side = 'left')
    

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

modifImage()
window.mainloop()
