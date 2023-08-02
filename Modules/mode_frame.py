import customtkinter

class PlaymodeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.draw()

    def draw(self):
        self.grid_columnconfigure(0, weight=0)
        self.configure(border_color = 'red', border_width=1)
        self.value = customtkinter.IntVar(value=self.master.cfg.current['random'])
        self.radios = []
        self.title = customtkinter.CTkLabel(self, text="Play mode", fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        checkbox = customtkinter.CTkCheckBox(self, text="Random", variable=self.value, onvalue=1, offvalue=0,                                                  command=self.selection_mode_handler)
        checkbox.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="ew")

    def selection_mode_handler(self):
        print(self.value.get())
        self.master.cfg.current['random'] = self.value.get()
        return self.value.get()