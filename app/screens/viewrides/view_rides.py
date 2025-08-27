import customtkinter as ctk
from tkinter import messagebox
import config.config_var as Config
from services.rideService import RideService

class ViewMyRidesPage(ctk.CTkFrame):
    def __init__(self, root, manager):
        super().__init__(root)
        self.manager = manager
        self.ride_service = RideService()

        # Title
        ctk.CTkLabel(self, text="My Rides", font=("Arial", 18, "bold")).pack(pady=15)

        # Scroll
        self.rides_frame = ctk.CTkScrollableFrame(self, corner_radius=12, width=400, height=300)
        self.rides_frame.pack(pady=15, padx=10, fill="both", expand=True)

        back_btn = ctk.CTkButton(
            self,
            text="Back",
            command=lambda: self.manager.show_screen("rider_dashboard") if self.manager else None,
            width=100,
            height=40,
            corner_radius=10,
            font=("Arial", 14)
        )
        back_btn.pack(pady=10)


    def clear_rides(self):
        """Clear old ride widgets"""
        for widget in self.rides_frame.winfo_children():
            widget.destroy()

    def cancel_ride(self, ride_id):
        try:
            success = self.ride_service.update_ride(ride_id, {"status": "cancelled"})
            if success:
                messagebox.showinfo("Success", f"Ride {ride_id} cancelled.")
                self.fetch_my_rides() 
            else:
                messagebox.showerror("Error", f"Could not cancel ride {ride_id}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error cancelling ride: {e}")
    
    def complete_ride(self, ride_id):
        try:
            success = self.ride_service.update_ride(ride_id, {"status": "completed"})
            if success:
                messagebox.showinfo("Success", f"Ride {ride_id} marked as completed.")
                self.fetch_my_rides()  
            else:
                messagebox.showerror("Error", f"Could not complete ride {ride_id}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error completing ride: {e}")


    def fetch_my_rides(self):
        """Fetch all rides for the logged-in user"""
        self.clear_rides()

        if not Config.loggedInUser:
            messagebox.showwarning("Warning", "No user is logged in!")
            return

        user_id = Config.loggedInUser["_id"]
        role = Config.loggedInUser.get("role", "")

        try:
             rides = self.ride_service.list_rides(role, user_id)
                    
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
            
            if status.lower() in ["requested", "accepted", "ongoing"]:
                ctk.CTkButton(
                    card,
                    text="Cancel Ride",
                    command=lambda ride_id=ride["_id"]: self.cancel_ride(ride_id),
                    fg_color="red",
                    hover_color="darkred"
                ).pack(pady=5, padx=10, anchor="e")
            
            if status.lower() == "ongoing":
                ctk.CTkButton(
                   card,
                   text="Complete Ride",
                   command=lambda ride_id=ride["_id"]: self.complete_ride(ride_id),
                   fg_color="green",
                   hover_color="darkgreen"
                ).pack(pady=5, padx=10, anchor="e")
        
        