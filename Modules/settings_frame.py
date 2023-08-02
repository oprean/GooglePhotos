import customtkinter
from tkinter import ttk
from program_frame import ProgramFrame
from scenes_frame import ScenesFrame
class SettingsFrame(customtkinter.CTkFrame):
    def __init__(self, parent, google, settings):
        super().__init__(parent)
        #self.grid_columnconfigure(4, weight=1)
        #self.grid_rowconfigure(3, weight=0)
        self.google = google
        self.cfg = settings
        self.draw()


    def draw(self):
        if (self.cfg.current['type']=="album"):
            self.state = "disabled"
        else:
            self.state = "normal"

        self.configure(border_color = 'green', border_width=1)
        if self.cfg.current["type"] == "album":
            self.albums = AlbumsSelectionFrame(self, self, values=self.google.albums)
            self.albums.grid(row=0, column=0, rowspan=3, sticky="ewns")
            self.albums.configure(fg_color="transparent")
        else:            
            self.categories = CategoriesSelectionFrame(self, values=self.google.categories)
            self.categories.grid(row=0, column=0, rowspan=3, sticky="ewns")
            self.categories.configure(fg_color="transparent")

        self.overlays = OverlaysFrame(self, values=['Title','Exif','Date','Description'])
        self.overlays.grid(row=1, column=1, sticky="ewns")
        self.overlays.configure(fg_color="transparent")

        playtype = GDFControl(self,"Play type","type", "radio")
        playtype.grid(row=0, column=1, sticky="ewns")
        playtype.configure(fg_color="transparent")

        random = GDFControl(self,"Random","random", "checkbox")
        random.grid(row=0, column=2, sticky="ewns")
        random.configure(fg_color="transparent")


        random = GDFControl(self,"Random","random", "checkbox")
        random.grid(row=0, column=2, sticky="ewns")
        random.configure(fg_color="transparent")

        remember = GDFControl(self,"Remember","remember", "radio")
        remember.grid(row=1, column=2, sticky="ewns")
        remember.configure(fg_color="transparent")

        favorites = GDFControl(self,"Favorites","favorites_only", "checkbox")
        favorites.grid(row=0, column=3, sticky="ewns")
        favorites.configure(fg_color="transparent")

        self.scenes = ScenesFrame(self)
        self.scenes.grid(row=0, column=4, sticky="ewns")
        self.scenes.configure(fg_color="transparent")

        self.program = ProgramFrame(self)
        self.program.grid(row=1, column=3, columnspan=2, sticky="ewns")
        self.program.configure(fg_color="transparent")

        duration = GDFControl(self,"Duration","duration", "spinbox")
        duration.grid(row=0, column=5, sticky="ewns")
        duration.configure(fg_color="transparent")

        # remember played items

        btnApplySettings = customtkinter.CTkButton(self, text="Apply", width=200, command=self.applySettings_callback).grid(row=2,column=4, padx=10, pady=10)
        #place(x=self.master.width-100,y=self.master.height-100)
        self.place(relx=0.5, rely=0.5, anchor="c")
    
    def applySettings_callback(self):
        self.cfg.save()
        self.master.main.tkraise()

class AlbumsSelectionFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, settings_frame, values):
        super().__init__(master, label_text="Albums")
        self.grid_columnconfigure(0, weight=0)
        self.configure(border_color = 'red', border_width=1)
        self.values = values
        self.settings_frame = settings_frame
        self.checkboxes = []
        self.draw()
    
    def draw(self):
        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value["title"], onvalue=value["id"], offvalue="", command=self.change_handler)
            if value["id"] in self.settings_frame.cfg.current["albums"]:
                checkbox.select()
            checkbox.grid(row=i, column=1, padx=10, pady=(10, 0), sticky="ew")
            self.checkboxes.append(checkbox)

    def change_handler(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() != "":
                checked_checkboxes.append(checkbox.get())
        print(checked_checkboxes)
        self.settings_frame.cfg.current["albums"] = checked_checkboxes
        return checked_checkboxes

class CategoriesSelectionFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, values):
        super().__init__(master, label_text="AI Categories")
        self.grid_columnconfigure(0, weight=0)
        self.configure(border_color = 'red', border_width=1)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value, state=master.state)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="ew")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

class OverlaysFrame(customtkinter.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=0)
        self.configure(border_color = 'red', border_width=1)
        self.values = values
        self.checkboxes = []
        self.title = customtkinter.CTkLabel(self, text="Overlays", fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="ew")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes    

class GDFControl(customtkinter.CTkFrame):
    def __init__(self, master, label, mapped_key, ctrl_type):
        super().__init__(master)
        self.ctrl_type = ctrl_type
        self.label = label
        self.mapped_key = mapped_key
        #self.value = None
        self.values = []
        self.setInitialValues()
        self.draw()

    def setInitialValues(self):
        if self.mapped_key in self.master.cfg.current.keys():
            vtype = type(self.master.cfg.current[self.mapped_key])
            if vtype == int:
                self.value = customtkinter.IntVar(value=self.master.cfg.current[self.mapped_key])
            elif vtype == str:
                self.value = customtkinter.StringVar(value=self.master.cfg.current[self.mapped_key])
            elif vtype == dict:
                self.values = customtkinter.StringVar(value=self.master.cfg.current[self.mapped_key])
            else:
                self.value = None
        if self.mapped_key in self.master.cfg.settings["sources"].keys():
            self.values = self.master.cfg.settings["sources"][self.mapped_key]
        else:
            self.values = None

    def draw(self):
        start_row = 0
        if (self.label != "" and self.ctrl_type != "checkbox"):
            self.title = customtkinter.CTkLabel(self, text=self.label, fg_color="gray30", corner_radius=6)
            self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
            start_row = 1
        self.grid_columnconfigure(0, weight=0)
        #self.configure(border_color = 'red', border_width=1)

        if (self.ctrl_type == "spinbox"):
            ctrl = ttk.Spinbox(self,from_=0,to=23,
                #values=hoursRange,
                textvariable=self.value,
                width=2,                
                wrap=True)
        elif(self.ctrl_type == 'checkbox'):
            ctrl = customtkinter.CTkCheckBox(self, text=self.label, variable=self.value, onvalue=1, offvalue=0, command=self.change_handler)

        elif(self.ctrl_type == 'radio'):
            ctrls = []
            for i, value in enumerate(self.values):
                ctrl = customtkinter.CTkRadioButton(self, text=value, variable=self.value, value=value, command=self.change_handler)
                #state=self.master.state, command=self.change_handler)
                ctrl.grid(row=start_row+i+1, column=0, padx=10, pady=(10, 0), sticky="ew")
                ctrls.append(ctrl)

        elif(self.ctrl_type == 'checkboxes'):
            ctrls = []
            for i, value in enumerate(self.values):
                ctrl = customtkinter.CTkRadioButton(self, text=value, variable=self.value, value=value, command=self.change_handler)
                #state=self.master.state, command=self.change_handler)
                ctrl.grid(row=start_row+i+1, column=0, padx=10, pady=(10, 0), sticky="ew")
                ctrls.append(ctrl)



        ctrl.grid(row=start_row, column=0, padx=10, pady=(10, 0), sticky="ew")

    def change_handler(self):
        self.master.cfg.current[self.mapped_key] = self.value.get()
        self.master.draw()
        print(self.mapped_key + ' || '+ str(self.value.get()))
        return self.value.get()

