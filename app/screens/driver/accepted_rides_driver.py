import customtkinter as ctk
from services.rideService import RideService
import config.config_var as config

class AcceptedRideRequestsDriver(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager
        self.ride_service = RideService()

        # Header
        header_frame = ctk.CTkFrame(self, height=60, fg_color="#1f6aa5")
        header_frame.pack(fill="x")
        header_label = ctk.CTkLabel(
            header_frame, 
            text="Accepted Rides", 
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
            if ride['status'] == "accepted" or ride['status'] == "in_progress":
                self.create_ride_tile(ride)

    def create_ride_tile(self, ride):
        tile = ctk.CTkFrame(
            self.scrollable_frame, 
            corner_radius=12, 
            border_width=1, 
            border_color="#cccccc",
            fg_color="#f0f0f0"
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

        # Action buttons
        btn_frame = ctk.CTkFrame(tile, fg_color="transparent")
        btn_frame.pack(side="right", padx=20, pady=10)

        if ride['status'] == "accepted":
            start_btn = ctk.CTkButton(btn_frame, text="Start Ride", fg_color="#4CAF50", hover_color="#45a049",
                                    command=lambda r=ride: self.start_ride(r))
            start_btn.pack(pady=5, fill="x")


        if ride['status'] != 'completed' or ride['status'] != 'cancelled' :
            cancel_btn = ctk.CTkButton(btn_frame, text="Cancel Ride", fg_color="#f44336", hover_color="#da190b",
                                        command=lambda r=ride: self.cancel_ride(r))
            cancel_btn.pack(pady=5, fill="x")

        if ride['status'] == 'in_progress':
            complete_btn = ctk.CTkButton(btn_frame, text="Complete Ride", fg_color="#2196F3", hover_color="#1976D2",
                                        command=lambda r=ride: self.complete_ride(r))
            complete_btn.pack(pady=5, fill="x")

    def start_ride(self, ride):
        try:
            ok = self.ride_service.update_ride(ride.get('_id'), {"status": "in_progress"})
            if ok:
                self.show_popup("✅ Ride started!", color="green")
        except Exception as e:
            self.show_popup(f"❌ Error: {e}", color="red")
        finally:
            self.load_accepted_rides()

    def cancel_ride(self, ride):
        try:
            ok = self.ride_service.update_ride(ride.get('_id'), {"status": "cancelled"})
            if ok:
                self.show_popup("✅ Ride cancelled!", color="green")
        except Exception as e:
            self.show_popup(f"❌ Error: {e}", color="red")
        finally:
            self.load_accepted_rides()

    def complete_ride(self, ride):
        try:
            ok = self.ride_service.update_ride(ride.get('_id'), {"status": "completed"})
            if ok:
                self.show_popup("✅ Ride completed!", color="green")
        except Exception as e:
            self.show_popup(f"❌ Error: {e}", color="red")
        finally:
            self.load_accepted_rides()

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