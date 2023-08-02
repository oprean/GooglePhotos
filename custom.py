import customtkinter
from google_photo_service import GooglePhotos

class SettingsFrame(customtkinter.CTkFrame):
    def __init__(self, master, google):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.google = google

        #self.selection_mode = customtkinter.CTkComboBox(self, values=["Albums", "Categories", "Remember"], command=self.selection_mode_callback)
        #self.selection_mode.grid(row=0, column=0, pady=(7, 0), sticky="new")
        #self.selection_mode.set("Albums")
        self.mode = SelectionModeFrame(self,values=["Albums", "Categories", "Remember"])
        self.mode.grid(row=0, column=3, pady=(7, 0), sticky="new")
        self.mode.configure(fg_color="transparent")

        self.albums = AlbumsSelectionFrame(self, values=self.google.albums)
        self.albums.grid(row=0, column=1, sticky="wns")
        self.albums.configure(fg_color="transparent")

        self.categories = AlbumsSelectionFrame(self, values=self.google.albums)
        self.categories.grid(row=0, column=1, sticky="wns")
        self.categories.configure(fg_color="transparent")

        self.overlay_infos = OverlaySelectionFrame(self, "Overlay infos", values=["Album tile", "EXIF info", "Date & time"])
        self.overlay_infos.grid(row=0, column=2, sticky="wns")
        self.overlay_infos.configure(fg_color="transparent")

        self.btnApply = customtkinter.CTkButton(self, text="Save settings", command=self.btnApply_callback)
        self.btnApply.grid(row=2, column=1, padx=10, pady=10, sticky="es")


    def selection_mode_callback(self,choice):
        print("combobox dropdown clicked:", choice)

    def btnApply_callback(self):
        print("settings:", self.multi_selection.get())

class SelectionModeFrame(customtkinter.CTkFrame):
    def __init__(self, master,values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.value = customtkinter.IntVar(value=0)
        self.values = values

        self.radios = []

        for i, value in enumerate(self.values):
            radio = customtkinter.CTkRadioButton(self, text=value, variable=self.value, value=i,
                                                  command=self.selection_mode_handler)
            radio.grid(row=i, column=1, padx=10, pady=(10, 0), sticky="ew")
            self.radios.append(radio)

    def selection_mode_handler(self):
        return self.value.get()

class AlbumSelectionFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value["title"])
            checkbox.grid(row=i, column=1, padx=10, pady=(10, 0), sticky="ew")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


class MultipleSelectionFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value["title"])
            checkbox.grid(row=i, column=1, padx=10, pady=(10, 0), sticky="ew")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("my app")
        self.grid_columnconfigure(0, weight=1)
        #self.attributes('-fullscreen',True)    
        self.geometry("400x220")
        self.grid_rowconfigure(0, weight=1)

        self.google = GooglePhotos()

        self.settings = SettingsFrame(self, self.google)
        self.settings.grid(row=0, column=0, sticky="nsew")

app = App()
app.mainloop()