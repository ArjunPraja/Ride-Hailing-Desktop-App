from logging import config
import customtkinter as ctk
import config.config_var as Config 
from app.utils.helpers import get_all_entries

class RiderDashboard(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main content frame
        self.content_frame = ctk.CTkFrame(self, bg_color="transparent")
        self.content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_rowconfigure(tuple(range(9)), weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkLabel(self.content_frame, text="Rider Dashboard", font=("Arial", 40))
        header.grid(row=0, column=0, pady=(20,30))

        # Buttons for functionalities
        btn_width = 250
        btn_height = 40
        font_btn = ("Arial", 16)

        self.btn_view_requests = ctk.CTkButton(self.content_frame, text="Request Ride", command=self.ride_request, width=btn_width, height=btn_height, font=font_btn)
        self.btn_view_requests.grid(row=1, column=0, pady=5)

        self.btn_view_my_rides = ctk.CTkButton(self.content_frame, text="View My Rides", command=self.view_my_rides, width=btn_width, height=btn_height, font=font_btn)
        self.btn_view_my_rides.grid(row=2, column=0, pady=5)

        self.btn_view_ride_by_id = ctk.CTkButton(self.content_frame, text="Logout", command=self.logout, width=btn_width, height=btn_height, font=font_btn)
        self.btn_view_ride_by_id.grid(row=3, column=0, pady=5)

        # Status label for messages
        self.status_label = ctk.CTkLabel(self.content_frame, text="", font=("Arial", 12))
        self.status_label.grid(row=4, column=0, pady=10)

    # ---------------- Placeholder methods ---------------- #

    def ride_request(self):
        self.manager.show_screen('ride_request')

    def view_my_rides(self):
        self.manager.show_screen('view_rides')
    
    def logout(self):
        Config.loggedInUser = None  
        self.status_label.configure(text="Logging out...")
        self.manager.show_screen("landing")
        
    def reset_screen(self):
        self.status_label.configure(text="")
        