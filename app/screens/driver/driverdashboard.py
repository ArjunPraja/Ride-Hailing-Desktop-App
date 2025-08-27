import customtkinter as ctk
import config.config_var as config

class DriverDashboard(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main content frame
        self.content_frame = ctk.CTkFrame(self, bg_color="transparent")
        self.content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_rowconfigure(tuple(range(6)), weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkLabel(self.content_frame, text="Driver Dashboard", font=("Arial", 40))
        header.grid(row=0, column=0, pady=(20,30))

        # Buttons for functionalities
        btn_width = 250
        btn_height = 40
        font_btn = ("Arial", 16)

        self.btn_view_requests = ctk.CTkButton(self.content_frame, text="View Ride Requests", command=self.view_ride_requests, width=btn_width, height=btn_height, font=font_btn)
        self.btn_view_requests.grid(row=1, column=0, pady=5)

        self.btn_view_my_rides = ctk.CTkButton(self.content_frame, text="My Rides", command=self.view_my_rides, width=btn_width, height=btn_height, font=font_btn)
        self.btn_view_my_rides.grid(row=2, column=0, pady=5)

        self.btn_view_vehicles = ctk.CTkButton(self.content_frame, text="My Vehicles", command=self.view_vehicles, width=btn_width, height=btn_height, font=font_btn)
        self.btn_view_vehicles.grid(row=3, column=0, pady=5)

        self.btn_logout = ctk.CTkButton(self.content_frame, text="Logout", command=self.logout, width=btn_width, height=btn_height, font=font_btn)
        self.btn_logout.grid(row=4, column=0, pady=5)

        # Status label for messages
        self.status_label = ctk.CTkLabel(self.content_frame, text="", font=("Arial", 12))
        self.status_label.grid(row=5, column=0, pady=10)

    # ---------------- Placeholder methods ---------------- #

    def view_ride_requests(self):
        print("1. View Ride Requests")
        self.status_label.configure(text="Viewing ride requests...")

    def view_my_rides(self):
        print("2. View My Rides")
        self.status_label.configure(text="Viewing your rides...")

    def view_vehicles(self):
        self.manager.show_screen('view_vehicles')

    def update_vehicle(self):
        self.manager.show_screen('vehicle_form')

    def logout(self):
        config.loggedInUser = None  
        self.status_label.configure(text="Logging out...")
        self.manager.show_screen("landing")
