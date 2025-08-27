import customtkinter as ctk
from services.rideService import RideService
import config.config_var as config
import random

class RideRequestPage(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager
        self.ride_service = RideService()

        # layout for outer frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # content frame (centered like in LoginPage)
        content_frame = ctk.CTkFrame(self, bg_color="transparent")
        content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        content_frame.grid_rowconfigure((0, 5), weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Title
        title = ctk.CTkLabel(content_frame, text="🚖 Request a Ride", font=("Arial", 32))
        title.grid(row=1, column=0, pady=(20, 30), sticky="n")

        # Pickup Location
        self.pickup_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Enter pickup location",
            width=300,
            height=40,
            corner_radius=8
        )
        self.pickup_entry.grid(row=2, column=0, padx=200, pady=10, sticky="ew")

        # Drop Location
        self.drop_entry = ctk.CTkEntry(
            content_frame,
            placeholder_text="Enter drop location",
            width=300,
            height=40,
            corner_radius=8
        )
        self.drop_entry.grid(row=3, column=0, padx=200, pady=10, sticky="ew")

        # Request Button
        request_btn = ctk.CTkButton(
            content_frame,
            text="Request Ride",
            command=self.request_ride,
            width=150,
            height=40,
            corner_radius=10,
            font=("Arial", 18)
        )
        request_btn.grid(row=4, column=0, pady=20)

        

        # Status Label
        self.status_label = ctk.CTkLabel(content_frame, text="", font=("Arial", 14))
        self.status_label.grid(row=5, column=0, pady=10)

        #Back
        back_btn = ctk.CTkButton(
            self,
            text="⬅ Back",
            command=lambda: self.manager.show_screen("rider_dashboard"),
            width=100,
            height=35
        )
        back_btn.grid(row=99, column=0, sticky="w", padx=10, pady=10)


    def request_ride(self):
        pickup = self.pickup_entry.get().strip()
        drop = self.drop_entry.get().strip()
        if not pickup or not drop:
            self.status_label.configure(text="⚠ Please fill in all fields.", text_color="red")
            return

        try:
            ride_data = {
                "rider_id": config.loggedInUser.get("_id"),
                "pickup_location": pickup,
                "drop_location": drop,
                "fare": random.randint(500, 1000),
                "status": "requested"
            }
            ride_id = self.ride_service.insert_ride(ride_data)
            self.status_label.configure(text=f"✅ Ride requested! ID: {ride_id}", text_color="green")
            self.show_popup(f"✅ Ride requested! ID: {ride_id}", color="green")
            self.manager.show_screen("view_ride_by_id", ride_id=ride_id)
            

        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {str(e)}", text_color="red")
    
      # ---------------- Sexy Pop-up function ----------------
    def show_popup(self, message, color="green"):
        popup = ctk.CTkToplevel(self)
        popup.geometry("400x180")
        popup.title("Notification")
        popup.grab_set()  # Make modal

        popup_label = ctk.CTkLabel(
            popup, 
            text=message, 
            font=("Arial", 18, "bold"), 
            text_color=color,
            wraplength=350,
            justify="center"
        )
        popup_label.pack(expand=True, pady=30, padx=20)

        ok_button = ctk.CTkButton(
            popup, 
            text="OK ✅", 
            width=100,
            height=40,
            font=("Arial", 14, "bold"),
            corner_radius=12,
            command=popup.destroy
        )
        ok_button.pack(pady=10)

    def reset_screen(self):
        self.pickup_entry.delete(0, "end")
        self.drop_entry.delete(0, "end")
        self.status_label.configure(text="")