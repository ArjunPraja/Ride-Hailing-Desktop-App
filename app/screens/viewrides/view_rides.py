import customtkinter as ctk
from tkinter import messagebox
from config.database import DatabaseConfig
import config.config_var as Config
from models.rideModel import RideModel
from bson import ObjectId

class ViewMyRidesPage(ctk.CTkFrame):
    def __init__(self, root, manager):
        super().__init__(root)
        self.manager = manager

        # Title
        ctk.CTkLabel(self, text="My Rides", font=("Arial", 18, "bold")).pack(pady=15)

        # Scroll
        self.rides_frame = ctk.CTkScrollableFrame(self, corner_radius=12, width=400, height=300)
        self.rides_frame.pack(pady=15, padx=10, fill="both", expand=True)

       
        

    def clear_rides(self):
        """Clear old ride widgets"""
        for widget in self.rides_frame.winfo_children():
            widget.destroy()

    def fetch_my_rides(self):
        """Fetch all rides for the logged-in user"""
        self.clear_rides()

        if not Config.loggedInUser:
            messagebox.showwarning("Warning", "No user is logged in!")
            return

        user_id = Config.loggedInUser["_id"]
        role = Config.loggedInUser.get("role", "")

        
       
        pipeline = []
        if role == "rider":
            pipeline = [{"$match": {"rider_id": user_id}}]
        elif role == "driver":
            pipeline = [{"$match": {"driver_id": user_id}}]
        try:
             rides = RideModel.list_all_data(pipeline)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching rides: {e}")
            return

        if not rides:
            ctk.CTkLabel(
                self.rides_frame,
                text="No rides found for your account",
                text_color="red"
            ).pack(pady=10)
            return

       #Each card
        for ride in rides:
            card = ctk.CTkFrame(self.rides_frame, corner_radius=10, fg_color="#f0e9e9")
            card.pack(fill="x", padx=10, pady=5)

            # Status color
            status = ride.get("status", "Unknown")
            color = "green" if status.lower() == "completed" else "orange" if status.lower() == "ongoing" else "red"

            # Labels inside card
            ctk.CTkLabel(card, text=f"Ride ID: {ride.get('_id')}", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(card, text=f"Pickup: {ride.get('pickup_location', 'N/A')}", anchor="w").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Drop: {ride.get('drop_location', 'N/A')}", anchor="w").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Fare: ₹{ride.get('fare', 0)}", anchor="w").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Status: {status}", text_color=color, anchor="w").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Date: {ride.get('ride_date', 'N/A')}", anchor="w").pack(anchor="w", padx=10)
            