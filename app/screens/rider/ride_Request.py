import customtkinter as ctk
from services.rideService import RideService
from config.config_var import Config


class RideRequestPage(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager
        self.ride_service = RideService()

        # Title
        title = ctk.CTkLabel(self, text="🚖 Request a Ride", font=("Arial", 26, "bold"))
        title.pack(pady=20)

        # Pickup Location
        self.pickup_entry = ctk.CTkEntry(self, placeholder_text="Enter pickup location")
        self.pickup_entry.pack(pady=10, padx=40, fill="x")

        # Drop Location
        self.drop_entry = ctk.CTkEntry(self, placeholder_text="Enter drop location")
        self.drop_entry.pack(pady=10, padx=40, fill="x")

        # Request Button
        request_btn = ctk.CTkButton(self, text="Request Ride", command=self.request_ride)
        request_btn.pack(pady=20)

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.manager.show_screen("view_my_rides")

    def request_ride(self):
        pickup = self.pickup_entry.get().strip()
        drop = self.drop_entry.get().strip()

        if not pickup or not drop:
            self.status_label.configure(text="⚠ Please fill in all fields.", text_color="red")
            return

        try:
            ride_data = {
                "rider_id": Config.loggedInUser.get("_id"), 
                "pickup_location": pickup,
                "drop_location": drop,
                "fare": 100,  # dummy fare for now
                "status": "requested"
            }
            ride_id = self.ride_service.insert_ride(ride_data)
            self.status_label.configure(text=f"✅ Ride requested! ID: {ride_id}", text_color="green")

        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {str(e)}", text_color="red")
