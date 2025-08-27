import customtkinter as ctk
from services.rideService import RideService
import config.config_var as config

class MyRidesDriver(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager
        self.ride_service = RideService()

        # Header
        header_frame = ctk.CTkFrame(self, height=60, fg_color="#1f6aa5")
        header_frame.pack(fill="x")
        header_label = ctk.CTkLabel(
            header_frame, 
            text="My Rides", 
            font=ctk.CTkFont(size=20, weight="bold"), 
            text_color="white"
        )
        header_label.pack(pady=15)

        # Button frame under header
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        # Back Button
        back_btn = ctk.CTkButton(btn_frame, text="⬅ Back", width=120, command=self.go_back)
        back_btn.pack(side="left")

        # Reload Button
        reload_btn = ctk.CTkButton(btn_frame, text="Reload", width=120, command=self.load_accepted_rides)
        reload_btn.pack(side="right")

        # Scrollable frame for ride tiles
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=700, height=500)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def go_back(self):
        if self.manager:
            self.manager.show_screen("driver_dashboard")

    def load_accepted_rides(self):
        # Clear existing tiles
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.accepted_rides = self.ride_service.list_rides("driver", config.loggedInUser.get('_id'))

        # Create tiles for each accepted ride
        for ride in self.accepted_rides:
            self.create_ride_tile(ride)

    def create_ride_tile(self, ride):

        status_colors = {
            "accepted": "#FFF8B5",    # soft yellow
            "completed": "#C8FACC",   # soft green
            "cancelled": "#FECACA",   # soft red/pink
            "in_progress": "#B5D7FF"      # soft blue
        }
        tile_color = status_colors.get(ride["status"].lower(), "#f0f0f0")  # Default gray

        tile = ctk.CTkFrame(
            self.scrollable_frame, 
            corner_radius=12, 
            border_width=1, 
            border_color="#cccccc",
            fg_color=tile_color
        )
        tile.pack(fill="x", pady=10, padx=10)

        # Ride details
        ride_date_str = ride["ride_date"].strftime("%d %b %Y, %I:%M %p")
        details = (
            f"Ride ID: {ride['_id']}\n"
            f"Pickup: {ride['pickup_location']}\n"
            f"Drop: {ride['drop_location']}\n"
            f"Fare: ₹{ride['fare']}\n"
            f"Status: {ride['status'].capitalize()}\n"
            f"Date: {ride_date_str}"
        )

        label = ctk.CTkLabel(tile, text=details, justify="left", anchor="w", font=ctk.CTkFont(size=14))
        label.pack(side="left", padx=20, pady=10, expand=True, fill="both")