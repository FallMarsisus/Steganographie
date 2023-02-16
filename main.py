from PIL import Image, ImageTk
from urllib.request import urlopen
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import time

"""imageFile = fd.askopenfile(filetypes=(('Png File', '*.png'), ("Jpg file", "*.jpg"), ("Bmp file", "*.bmp")))
secretImageFile = fd.askopenfile(filetypes=(('Png File', '*.png'), ("Jpg file", "*.jpg"), ("Bmp file", "*.bmp")))"""

imageURL = "https://www.radiofrance.fr/s3/cruiser-production/2022/06/5f6ac5ab-37d9-4ca6-8f79-3694fcfec071/560x315_paysage-monet.jpg"
secretImageURL = r"https://media.lesechos.com/api/v1/images/view/6203b47f8fe56f43fc4f5a66/1280x720/070889361477-web-tete.jpg"

image = Image.open(urlopen(imageURL))
image = image.convert("RGB")

if image.width >= 500:
    image.thumbnail((500,500))

imageSecret = Image.open(urlopen(secretImageURL))
maxSize = (image.width, image.height)
imageSecret = imageSecret.resize(maxSize)
imageSecret = imageSecret.convert("RGB")


window = tk.Tk()
window.title("Stéganographe")

frame = tk.Frame(window)
frame.pack(expand=tk.TRUE)

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

textFinal = tk.Label(frameImages, text='=>', font=("Calibri", 25))
textFinal.pack(side = "left")

frameLoading = tk.Frame(frameImages, width=image.width, border=10)
frameLoading.pack(side="right", fill=tk.X)

textLoading = tk.Label(frameLoading, text='Patientez...', font=('Calibri', 12), width=image.width)
textLoading.pack()

progressbar = ttk.Progressbar(frameLoading, length=100, mode='determinate')
progressbar.pack(fill=tk.X)



# On encode
def encode():
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
                    elif l>=8: finalColorBin+= "0"

                finalColorBin = int(finalColorBin, 2)
                newPixel.append(finalColorBin)

            # print(f"{pixel} -> {newPixel}")
            newPixel = tuple(newPixel)

            image.putpixel((i,j), newPixel)


    

    # On décode
def decode():
    for i in range(image.width):
        for j in range(image.height):
            pixel = image.getpixel((i, j))

            newPixel = list()

            for k in range(len(pixel)):
                secretColorBin = bin(pixel[k])
                finalColorBin = "0b"

                for l in range(len(secretColorBin)):
                    if l>=len(secretColorBin) - 4>=6:
                        finalColorBin += secretColorBin[l]

                while len(finalColorBin)<10:
                    finalColorBin+='0'


                finalColorBin = int(finalColorBin, 2)
                newPixel.append(finalColorBin)

            newPixel = tuple(newPixel)

            image.putpixel((i,j), newPixel)
    image.show("Image décodée.png")

encode()


imageFinalTk = ImageTk.PhotoImage(image)
progressbar.pack_forget()
textLoading.pack_forget()
imageFinal = tk.Label(frameLoading, image=imageFinalTk)
imageFinal.pack(side = 'left')
buttonDecode= tk.Button(frame, text='Décoder', command=decode, font=("Calibri", 15))
buttonDecode.pack(pady=10)
window.mainloop()
