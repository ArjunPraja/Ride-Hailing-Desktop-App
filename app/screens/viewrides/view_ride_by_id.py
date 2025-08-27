import customtkinter as ctk
from tkinter import messagebox
import config.config_var as Config
from bson.errors import InvalidId
from services.rideService import RideService

class ViewRideByIdPage(ctk.CTkFrame):
    def __init__(self, root, manager):
        super().__init__(root)
        self.manager = manager
        self.ride_service = RideService()

        # Title
        ctk.CTkLabel(self, text="Ride Details", font=("Arial", 18, "bold")).pack(pady=15)

        # Scroll Frame for ride details
        self.details_frame = ctk.CTkScrollableFrame(self, corner_radius=12, width=380, height=250)
        self.details_frame.pack(pady=15, padx=10, fill="both", expand=True)

        back_btn = ctk.CTkButton(
            self,
            text="⬅ Back",
            command=lambda: self.manager.show_screen("rider_dashboard") if self.manager else None,
            width=100,
            height=35
        )
        back_btn.pack(pady=10, anchor="w", padx=10)


    def clear_details(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

    def add_detail(self, label, value, text_color=None, bold=False):
        row = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=2)

        font_style = ("Arial", 11, "bold") if bold else ("Arial", 11)
        ctk.CTkLabel(row, text=f"{label}:", width=80, anchor="w", font=font_style).pack(side="left")
        ctk.CTkLabel(row, text=value, anchor="w", text_color=text_color).pack(side="left")

    def fetch_ride(self, ride_id=None):
        self.clear_details()

        if not ride_id:
            messagebox.showwarning("Input Error", "No Ride ID provided")
            return

        try:
            ride = self.ride_service.get_ride(
                ride_id,
                Config.loggedInUser["role"],
                Config.loggedInUser["_id"]
            )

        except InvalidId:
            messagebox.showerror("Invalid ID", "Please enter a valid Ride ID format.")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching ride: {e}")
            return

        if not ride:
            ctk.CTkLabel(
                self.details_frame,
                text=f"No ride found with ID {ride_id} for your account",
                text_color="red"
            ).pack(pady=10)
            return

        # Show ride details
        self.add_detail("Ride ID", str(ride.get('_id')), bold=True)
        self.add_detail("Pickup", ride.get("pickup_location", "N/A"))
        self.add_detail("Drop", ride.get("drop_location", "N/A"))
        self.add_detail("Fare", f"₹{ride.get('fare', 0)}")

        status = ride.get("status", "Unknown")
        color = "green" if status.lower() == "completed" else "orange" if status.lower() == "ongoing" else "red"
        self.add_detail("Status", status, text_color=color, bold=True)

        self.add_detail("Date", str(ride.get("ride_date", "N/A")))
