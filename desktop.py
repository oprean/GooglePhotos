# Import library
import tkinter as tk
from PIL import Image, ImageTk, ImageOps, ImageFont, ImageDraw 
import requests
import time

from google_photo_service import GooglePhotos

class DigitalFrameWnd():
    def __init__(self):
        # Create window Tkinter
        self.window = tk.Tk()      
        # Name our Tkinter application title
        self.window.title(" Google Photos Digital Frame ... ")
        self.window.attributes('-fullscreen',True)    

        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()

        self.lblImage = tk.Label(self.window)
        self.lblImage.place(x=-2, y=-2)

        #self.lblAlbumName = tk.Label(self.window, text="",font=('Calibri 15 bold'))
        #self.lblAlbumName.place(x=100, y=0)

        self.btnPrev = tk.Button(self.window, text="Prev", command=self.on_click_prev)
        self.btnPrev.place(x=10, y=10)

        self.btnNext = tk.Button(self.window, text="Next", command=self.on_click_next)
        self.btnNext.place(x=50, y=10)

        self.btnPrev = tk.Button(self.window, text="close", command=self.on_click_close)
        self.btnPrev.place(x=10, y=50)
        
        self.google = GooglePhotos()
        self.albumNo = 0
        self.itemNo = 0
        self.prev_img = None
        self.selectedAlbum = None
        self.selectedPhoto = None
        self.updateCurrent(self.albumNo, self.itemNo)
    
    def updateCurrent(self, albumNo, itemNo):
        if (self.albumNo != albumNo or not self.selectedAlbum):
            self.albumNo = albumNo
            self.selectedAlbum = self.google.albums[self.albumNo]
            self.selectedAlbum['items'] = self.google.getAlbumItems(self.selectedAlbum['id'])
            #self.selectedAlbum['items'] = self.google.getFilteredItems({"ses":"dddd"})

        self.itemNo = itemNo
        self.selectedPhoto = self.selectedAlbum['items'][self.itemNo]
        #self.lblAlbumName["text"] = self.selectedAlbum['title'] + " | "+ str(self.itemNo)
        self.updateImage()

    def padding(self, img):
        desired_size = (self.width, self.height)
        delta_width = desired_size[0] - img.size[0]
        delta_height = desired_size[1] - img.size[1]
        pad_width = delta_width // 2
        pad_height = delta_height // 2
        padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
        return ImageOps.expand(img, padding)

    def updateImage(self):
        append = "=w"+str(self.width)
        if (self.selectedPhoto["mediaMetadata"]["height"] > self.selectedPhoto["mediaMetadata"]["width"]):
            append = "=h"+str(self.height)
        url = self.selectedPhoto["baseUrl"]+append
        #url = self.selectedPhoto["baseUrl"]+"=w"+str(self.width)
        new_img = Image.open(requests.get(url, stream=True).raw)
        new_img = self.padding(new_img)
        draw = ImageDraw.Draw(new_img) 
        font = ImageFont.truetype(r'c:\Personal\projects\PythonDigitalFrame\GooglePhotos\Data\notoserif_bold_italic.ttf', 20) 
        draw.text((0, self.height-30), self.selectedAlbum['title'], font=font, align ="right")

        if (self.prev_img != None):
            alpha = 0
            while 1.0 > alpha:
                try:
                    current_img = Image.blend(self.prev_img,new_img,alpha)
                except Exception as ex:
                    print(ex)
                alpha = alpha + 0.1
                time.sleep(0.001)
                current_img = ImageTk.PhotoImage(current_img)
                self.lblImage.configure(image=current_img)
                self.lblImage.image=current_img
                self.lblImage.update()
        else:
            img = ImageTk.PhotoImage(new_img)
            self.lblImage.configure(image=img)
            self.lblImage.image=img
            self.lblImage.update()

        self.prev_img = new_img

    def on_click_next(self):      
        itemNo = self.itemNo + 1  
        self.updateCurrent(self.albumNo,itemNo)

        

    def on_click_prev(self):
        itemNo = self.itemNo - 1  
        self.updateCurrent(self.albumNo,itemNo)


    def on_click_close(self):
        self.window.destroy()

    def slideshow(self):
        self.window.after(3, self.slideshow)
        itemNo = self.itemNo + 1  
        self.updateCurrent(self.albumNo,itemNo)
        return
        while True:
            time.sleep(3)
            time_text=time.strftime("%d/%m/%Y %A %H:%M:%S")
            itemNo = self.itemNo + 1  
            self.updateCurrent(self.albumNo,itemNo)

    def start(self):
        #self.window.after(0, self.slideshow)
        #self.slideshow()
        self.window.mainloop()
# Run main loop
mainWnd = DigitalFrameWnd()
mainWnd.start()
 
