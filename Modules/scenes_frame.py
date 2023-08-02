import customtkinter
from CTkMessagebox import CTkMessagebox

class ScenesFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.draw()

    def draw(self):
        self.grid_columnconfigure(4, weight=0)
        self.configure(border_color = 'red', border_width=1)
        self.value = customtkinter.StringVar(value=self.master.cfg.current["name"])
        self.values = self.master.cfg.settings["scenes"]
        self.radios = []
        self.title = customtkinter.CTkLabel(self, text="Scenes", fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, columnspan=5, padx=10, pady=(10, 0), sticky="ew")

        frmButtons = customtkinter.CTkFrame(self)
        frmButtons.grid_columnconfigure(4, weight=1)
        frmButtons.grid(row=len(self.values)+2, column=0, padx=10, pady=10)
        
        btnSave = customtkinter.CTkButton(frmButtons, text="Save", width=50, command=self.save_callback).grid(row=1, column=0, pady=2, padx=2)
        btnRename = customtkinter.CTkButton(frmButtons, text="Rename", width=50, command=self.rename_callback).grid(row=1, column=1, pady=2, padx=2)
        btnNew = customtkinter.CTkButton(frmButtons, text="New", width=50, command=self.new_callback).grid(row=1, column=2, pady=2, padx=2)
        btnDelete = customtkinter.CTkButton(frmButtons, text="Delete", width=50, command=self.delete_callback).grid(row=1, column=3, pady=2, padx=2)

        for i, value in enumerate(self.values):
            radio = customtkinter.CTkRadioButton(self, text=value["name"], variable=self.value, value=value["name"],
                                                  command=self.select_callback)
            radio.grid(row=i+2, column=0, padx=10, pady=(10, 0), sticky="ew")
            self.radios.append(radio)

    def select_callback(self):
        print(self.value.get())
        self.master.cfg.setCurrent(self.value.get())
        self.master.draw()
            
    def save_callback(self):
        return self.value.get()
    
    def rename_callback(self):
        dialog = customtkinter.CTkInputDialog(text="Name:", title="Rename scene as ...")
        print("Name:", dialog.get_input())

    def new_callback(self):
        #https://github.com/Akascape/CTkMessagebox
        if len(self.master.cfg.settings["scenes"]) > 5:
            CTkMessagebox(title="Warning Message!", message="You can not add anymore scenes!",
                  icon="warning", option_1="Ok")
        else:
            dialog = customtkinter.CTkInputDialog(text="Name:", title="Save new scene as ...")
            self.master.cfg.appendScene(dialog.get_input())
            self.draw()

    def delete_callback(self):
        return self.value.get()
