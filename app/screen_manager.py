import customtkinter as ctk

class ScreenManager(ctk.CTk):
    def __init__(self, root):
        self.root = root
        self.screens = {}

    def add_screen(self, name, screen_class):
        screen = screen_class(self.root, self)  # Pass root and manager
        self.screens[name] = screen
        screen.grid(row=0, column=0, sticky="nsew")  # Stack on root
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def show_screen(self, name):
        screen = self.screens.get(name)
        if screen:
            screen.tkraise()