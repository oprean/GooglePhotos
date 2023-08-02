from tkinter import ttk
import tkinter as tk
import customtkinter
from PIL import Image, ImageTk, ImageOps, ImageFont, ImageDraw 
import requests
import time
import os
import random

FONT_PATH = os.getcwd() + "\\Data/notoserif_bold_italic.ttf"

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, parent, google, settings):
        super().__init__(parent)
        #self.grid_columnconfigure(0, weight=1)
        self.configure(border_color = 'red', border_width=1)
        self.google = google
        self.cfg = settings
        self.albumNo = 0
        self.itemNo = 0
        self.prev_img = None
        self.selectedAlbum = None
        self.selectedPhoto = None

        self.lblImage = tk.Label(self)
        self.lblImage.grid(row=0, column=0, columnspan=4, sticky="ewns")
        
        self.grid(row=0, column=0, sticky="ewns")
        self.updateCurrent(self.albumNo, self.itemNo)
        btnToggleMenu = customtkinter.CTkButton(self, text="M", width=20, height=20, command=self.showSettingFrame_callback).place(x=10,y=10)

        self.after(3000, self.nextItem)

    def setNextValues(self):
        current = self.cfg.current
        if current['type'] == "album":
            albums = self.cfg.current['albums']
            self.albumNo = random.randint(0,len(albums)-1)

    def nextItem(self):
        itemNo = self.itemNo + 1
        albumNo = self.albumNo
        self.updateCurrent(albumNo, itemNo)
        self.after(3000, self.nextItem)

    def showSettingFrame_callback(self):
        self.master.settings.tkraise()

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
        desired_size = (self.master.width, self.master.height)
        delta_width = desired_size[0] - img.size[0]
        delta_height = desired_size[1] - img.size[1]
        pad_width = delta_width // 2
        pad_height = delta_height // 2
        padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
        return ImageOps.expand(img, padding)

    def updateImage(self):
        append = "=w"+str(self.master.width)
        if (self.selectedPhoto["mediaMetadata"]["height"] > self.selectedPhoto["mediaMetadata"]["width"]):
            append = "=h"+str(self.master.height)
        url = self.selectedPhoto["baseUrl"]+append
        #url = self.selectedPhoto["baseUrl"]+"=w"+str(self.width)
        new_img = Image.open(requests.get(url, stream=True).raw)
        new_img = self.padding(new_img)
        draw = ImageDraw.Draw(new_img) 
        font = ImageFont.truetype(FONT_PATH, 20) 
        draw.text((0, self.master.height-30), self.selectedAlbum['title'], font=font, align ="right")

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