import sys
import customtkinter
import os

ROOT_PATH = os.getcwd()
sys.path.append(ROOT_PATH+"\\Modules")
from google_photo_service import GooglePhotos
from configuration import GDFConfiguration

from main_frame import MainFrame
from settings_frame import SettingsFrame

SETTINGS_JSON = ROOT_PATH + "\\Data\\settings.json"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("My Digital Frame")
        #self.grid_columnconfigure(0, weight=1)
        #self.grid_rowconfigure(0, weight=1)
        #self.attributes('-fullscreen',True)    
        self.geometry("1500x800")

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

        self.google = GooglePhotos()

        self.cfg = GDFConfiguration(SETTINGS_JSON)
        print(self.cfg.current)

        self.settings = SettingsFrame(self, self.google, self.cfg)
        self.main = MainFrame(self, self.google, self.cfg)

    def start(self):
        self.mainloop()

app = App()
app.start()
