import customtkinter

class FavoritesFrame(customtkinter.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=0)
        self.configure(border_color = 'red', border_width=1)
        self.value = customtkinter.IntVar(value=self.master.cfg.current['favorites_only'])
        self.title = customtkinter.CTkLabel(self, text="Favorites", fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")

        checkbox = customtkinter.CTkCheckBox(self, text="Only favorite", variable=self.value, onvalue=1, offvalue=0, command=self.selection_mode_handler)
        checkbox.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="ew")

    def selection_mode_handler(self):
        self.master.cfg.current['favorites_only'] = self.value.get()
        return self.value.get()    