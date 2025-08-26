import customtkinter as ctk
from tkinter import messagebox
from config.database import DatabaseConfig
from config import Config
from bson import ObjectId
from bson.errors import InvalidId


class ViewRideByIdPage(ctk.CTkFrame):
    def __init__(self, root, manager):
        super().__init__(root)
        self.manager = manager

        # Title
        ctk.CTkLabel(self, text="View Ride by ID", font=("Arial", 18, "bold")).pack(pady=15)

        # Input
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter Ride ID", width=280)
        self.entry.pack(pady=10)

        # Button
        ctk.CTkButton(self, text="Fetch Ride", command=self.fetch_ride).pack(pady=10)

        # Scroll Frame
        self.details_frame = ctk.CTkScrollableFrame(self, corner_radius=12, width=380, height=250)
        self.details_frame.pack(pady=15, padx=10, fill="both", expand=True)

        # Back Button
        # ctk.CTkButton(self, text="⬅ Back", command=lambda: self.manager.show_screen("rider_home")).pack(pady=5)

    def clear_details(self):
        """Clear previous ride details"""
        for widget in self.details_frame.winfo_children():
            widget.destroy()

    def add_detail(self, label, value, text_color=None, bold=False):
        """Helper to add detail row in card style"""
        row = ctk.CTkFrame(self.details_frame, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=2)

        font_style = ("Arial", 11, "bold") if bold else ("Arial", 11)
        ctk.CTkLabel(row, text=f"{label}:", width=80, anchor="w", font=font_style).pack(side="left")
        ctk.CTkLabel(row, text=value, anchor="w", text_color=text_color).pack(side="left")

    def fetch_ride(self):
        self.clear_details()
        ride_id = self.entry.get().strip()

        if not ride_id:
            messagebox.showwarning("Input Error", "Please enter a Ride ID")
            return

        try:
            db = DatabaseConfig.get_database()
            collection = db["rides"]

            query = {"_id": ObjectId(ride_id)}
            if Config.loggedInUser["role"] == "rider":
                query["rider_id"] = str(Config.loggedInUser["_id"])
            elif Config.loggedInUser["role"] == "driver":
                query["driver_id"] = str(Config.loggedInUser["_id"])

            ride = collection.find_one(query)
            print("Querying with:", query)
            print("Ride found:", ride)

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

    # show ride details
        self.add_detail("Ride ID", str(ride.get('_id')), bold=True)
        self.add_detail("Pickup", ride.get("pickup_location", "N/A"))
        self.add_detail("Drop", ride.get("drop_location", "N/A"))
        self.add_detail("Fare", f"₹{ride.get('fare', 0)}")

        # Status
        status = ride.get("status", "Unknown")
        color = "green" if status.lower() == "completed" else "orange" if status.lower() == "ongoing" else "red"
        self.add_detail("Status", status, text_color=color, bold=True)

        self.add_detail("Date", str(ride.get("ride_date", "N/A")))

        # Clear entry
        self.entry.delete(0, "end")
