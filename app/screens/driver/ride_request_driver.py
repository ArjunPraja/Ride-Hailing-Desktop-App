import customtkinter as ctk
from services.rideService import RideService
import config.config_var as config
from datetime import datetime, timezone

class RideRequestDriver(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager
        self.ride_service = RideService()

        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content = ctk.CTkFrame(self, bg_color="transparent")
        self.content.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        # Top bar: Back + Title + Reload
        topbar = ctk.CTkFrame(self.content, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew")
        topbar.grid_columnconfigure(0, weight=0)
        topbar.grid_columnconfigure(1, weight=1)
        topbar.grid_columnconfigure(2, weight=0)

        back_btn = ctk.CTkButton(topbar, text="⬅ Back", width=80, command=self.go_back)
        back_btn.grid(row=0, column=0, sticky="w", padx=4, pady=(6,8))

        title = ctk.CTkLabel(topbar, text="Ride Requests", font=("Arial", 28))
        title.grid(row=0, column=1, sticky="n", pady=(6,8))

        reload_btn = ctk.CTkButton(topbar, text="Reload", width=100, command=self.load_requests)
        reload_btn.grid(row=0, column=2, sticky="e", padx=4, pady=(6,8))

        # Scrollable table
        self.table = ctk.CTkScrollableFrame(self.content, label_text="")
        self.table.grid(row=1, column=0, sticky="nsew", pady=(10,0))

        # 7 columns: Rider, Pickup, Destination, Fare, Status, Action
        self.table.grid_columnconfigure((0,1,2,3,4,5), weight=1)

        # Status/info line
        self.info = ctk.CTkLabel(self.content, text="", font=("Arial", 12))
        self.info.grid(row=2, column=0, pady=(8,0))

        # Initial load
        self.load_requests()

    def go_back(self):
        self.manager.show_screen("driver_dashboard")

    def clear_table(self):
        for w in self.table.winfo_children():
            w.destroy()

    def load_requests(self):

        self.clear_table()

        # Header
        headers = ["Rider ID", "Pickup", "Destination", "Fare", "Status", "Action"]
        for col, text in enumerate(headers):
            ctk.CTkLabel(self.table, text=text, font=("Arial", 14, "bold")).grid(
                row=0, column=col, padx=8, pady=6, sticky="nsew"
            )

        try:
            rides = self.ride_service.list_all_rides()
        except Exception as e:
            self.info.configure(text=f"❌ Error loading rides: {e}", text_color="red")
            return

        if not rides:
            ctk.CTkLabel(self.table, text="No ride requests right now.").grid(
                row=1, column=0, columnspan=len(headers), pady=14
            )
            self.info.configure(text="All clear ✨", text_color="white")
            return

        # Rows
        r = 1
        for ride in rides:
            if ride['status'] == "requested":
                # Show details
                ctk.CTkLabel(self.table, text=str(ride.get("rider_id", "N/A"))).grid(row=r, column=0, padx=8, pady=6, sticky="nsew")
                ctk.CTkLabel(self.table, text=str(ride.get("pickup_location", "N/A"))).grid(row=r, column=1, padx=8, pady=6, sticky="nsew")
                ctk.CTkLabel(self.table, text=str(ride.get("drop_location", "N/A"))).grid(row=r, column=2, padx=8, pady=6, sticky="nsew")
                ctk.CTkLabel(self.table, text=f"₹{ride.get('fare', 0)}").grid(row=r, column=3, padx=8, pady=6, sticky="nsew")
                ctk.CTkLabel(self.table, text=str(ride.get("status", "")).capitalize()).grid(row=r, column=4, padx=8, pady=6, sticky="nsew")

                # Accept button (only if still requested)
                accept_btn = ctk.CTkButton(
                    self.table, text="Accept", width=90,
                    command=lambda rid=str(ride["_id"]): self.accept_ride(rid)
                )
                accept_btn.grid(row=r, column=5, padx=6, pady=6, sticky="ew")

                r += 1

        self.info.configure(text=f"Loaded {len(rides)} request(s).", text_color="white")

    def accept_ride(self, ride_id: str):
        try:
            ok = self.ride_service.update_ride(ride_id, {"status": "accepted", "driver_id": config.loggedInUser.get('_id'), "updated_at":datetime.now(timezone.utc)})
            if ok:
                self.show_popup("✅ Ride accepted!", color="green")
            else:
                self.show_popup("⚠️ Ride was already taken or changed.", color="orange")
        except Exception as e:
            self.show_popup(f"❌ Error: {e}", color="red")
        finally:
            self.load_requests()

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
