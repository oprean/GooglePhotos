from tkinter import ttk
import customtkinter

class ProgramFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        #self.grid_columnconfigure(4, weight=0)
        self.configure(border_color = 'red', border_width=1)
        self.value = customtkinter.StringVar(value='0')
        programs = master.cfg.settings["program"]
        scenes = []
        for scene in master.cfg.settings["scenes"]:
            scenes.append(scene["name"])

        self.title = customtkinter.CTkLabel(self, text="Program", fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, columnspan=6, padx=10, pady=(10, 0), sticky="ew")

        btnSave = customtkinter.CTkButton(self, text="Add", width=50, command=self.new_callback).grid(row=len(programs)+2, column=0, sticky="ew", padx=10, pady=10)
        btnNew = customtkinter.CTkButton(self, text="Save", width=50, command=self.save_callback).grid(row=len(programs)+2, column=1, sticky="ew", padx=10, pady=10)

        lblStart = customtkinter.CTkLabel(self, text="Start time", fg_color="gray30", corner_radius=6)
        lblStart.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")

        lblEnd = customtkinter.CTkLabel(self, text="End time", fg_color="gray30", corner_radius=6)
        lblEnd.grid(row=1, column=2, columnspan=2, padx=10, pady=(10, 0), sticky="ew")

        lblScene = customtkinter.CTkLabel(self, text="Scene", fg_color="gray30", corner_radius=6)
        lblScene.grid(row=1, column=4, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(programs):

            spin_box_hour_from = ttk.Spinbox(self,from_=0,to=23,
                #values=hoursRange,
                #textvariable=self.value,
                width=2,
                wrap=True)
            spin_box_hour_from.grid(row=i+2, column=0, padx=10, pady=(10, 0), sticky="ew")
            spin_box_min_from = ttk.Spinbox(self,from_=0,to=59,
                #values=minsRange,
                #textvariable=self.value,
                width=2,
                wrap=True)
            spin_box_min_from.grid(row=i+2, column=1, padx=10, pady=(10, 0), sticky="ew")
            
            spin_box_hour_to = ttk.Spinbox(self,from_=0,to=23,
                #values=hoursRange,
                #textvariable=self.value,
                width=2,                
                wrap=True)
            spin_box_hour_to.grid(row=i+2, column=2, padx=10, pady=(10, 0), sticky="ew")
            spin_box_min_to = ttk.Spinbox(self,from_=0,to=59,
                #values=minsRange,
                #textvariable=self.value,
                width=2,                
                wrap=True)
            spin_box_min_to.grid(row=i+2, column=3, padx=10, pady=(10, 0), sticky="ew")

            cbx_scene = customtkinter.CTkComboBox(self, values=scenes,
                                     command=self.select_callback, variable=self.value)
            cbx_scene.grid(row=i+2, column=4, padx=10, pady=(10, 0), sticky="ew")

            btnRemove = customtkinter.CTkButton(self, text="Del", width=40, command=self.delete_callback).grid(row=i+2, column=5, padx=5, pady=(10, 0), sticky="ew")
    def select_callback(self):
        return self.value.get()
    def save_callback(self):
        return self.value.get()
    def new_callback(self):
        return self.value.get()
    def delete_callback(self):
        return self.value.get()