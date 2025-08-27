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

    def show_screen(self, name, **kwargs):
        screen = self.screens.get(name)
        if screen:

            #clearing the old data - for now...
            if hasattr(screen, "reset_screen"):
                screen.reset_screen()

            if hasattr(screen, "fetch_my_rides"):
                screen.fetch_my_rides()
            
            if hasattr(screen, "fetch_ride") and "ride_id" in kwargs:
                screen.fetch_ride(kwargs["ride_id"])
            
            if hasattr(screen, "load_accepted_rides"):
                screen.load_accepted_rides()
            
            if hasattr(screen, "load_ratings"):
                screen.load_ratings()

            # if screen supports reloading with data
            if hasattr(screen, "load_vehicle_data") and "vehicle_data" in kwargs:
                screen.vehicle_data = kwargs["vehicle_data"]
                screen.load_vehicle_data(kwargs["vehicle_data"])
            
            # if screen supports reloading with data
            elif hasattr(screen, "load_vehicles"):
                screen.load_vehicles()
            screen.tkraise()