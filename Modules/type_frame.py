import customtkinter

class TypeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.draw()

    def draw(self):
        self.grid_columnconfigure(0, weight=0)
        self.configure(border_color = 'red', border_width=1)
        self.values = ['album','filter']
        self.value = customtkinter.StringVar(value=self.master.cfg.current['type'])
        self.radios = []
        self.title = customtkinter.CTkLabel(self, text="Play type", fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            radio = customtkinter.CTkRadioButton(self, text=value, variable=self.value, value=value,
                                                  command=self.selection_mode_handler)
            radio.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="ew")
            self.radios.append(radio)

    def selection_mode_handler(self):
        print(self.value.get())
        self.master.cfg.current['type'] = self.value.get()
        self.master.draw()