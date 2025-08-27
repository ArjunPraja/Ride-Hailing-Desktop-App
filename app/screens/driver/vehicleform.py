import customtkinter as ctk
import config.config_var as config
from services.vehicleService import VehicleService

class VehicleForm(ctk.CTkFrame):
    def __init__(self, parent, manager=None, vehicle_data=None):
        super().__init__(parent)
        self.manager = manager
        self.vehicle_data = vehicle_data

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main content frame
        self.content_frame = ctk.CTkFrame(self, bg_color="transparent")
        self.content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_rowconfigure((0,10), weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        back_btn = ctk.CTkButton(
            self.content_frame, 
            text="⬅ Back", 
            width=70, 
            command=self.go_back
        )
        back_btn.grid(row=0, column=0, sticky="w", padx=12, pady=(8,5))

        # Header
        mode_text = "Vehicle"
        label = ctk.CTkLabel(self.content_frame, text=mode_text, font=("Arial", 40))
        label.grid(row=1, column=0, pady=(20,30), sticky="n")

        # Brand
        self.brand_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Enter brand", width=250, height=40, corner_radius=8)
        self.brand_entry.grid(row=2, column=0, padx=200, pady=10, sticky="ew")

        # Model
        self.model_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Enter model", width=250, height=40, corner_radius=8)
        self.model_entry.grid(row=3, column=0, padx=200, pady=10, sticky="ew")

        # Year
        self.year_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Enter year", width=250, height=40, corner_radius=8)
        self.year_entry.grid(row=4, column=0, padx=200, pady=10, sticky="ew")

        # Registration Number
        self.registration_no_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Enter registration number", width=250, height=40, corner_radius=8)
        self.registration_no_entry.grid(row=5, column=0, padx=200, pady=10, sticky="ew")

        # Color
        self.color_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Enter color", width=250, height=40, corner_radius=8)
        self.color_entry.grid(row=6, column=0, padx=200, pady=10, sticky="ew")

        # Action button (Register / Update)
        button_text = "Update Vehicle" if self.vehicle_data else "Create Vehicle"
        self.action_btn = ctk.CTkButton(
            self.content_frame, 
            text=button_text, 
            command=self.handle_submit, 
            width=150, 
            height=40, 
            corner_radius=10, 
            font=("Arial", 20)
        )
        self.action_btn.grid(row=7, column=0, pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(self.content_frame, text="", font=("Arial", 12))
        self.status_label.grid(row=8, column=0, pady=5)

        # Preload data if updating
        if self.vehicle_data:
            self.load_vehicle_data(self.vehicle_data)

    def load_vehicle_data(self, vehicle):

        # Clear previous entries
        self.brand_entry.delete(0, "end")
        self.model_entry.delete(0, "end")
        self.year_entry.delete(0, "end")
        self.registration_no_entry.delete(0, "end")
        self.color_entry.delete(0, "end")

        """Pre-fill fields if vehicle_data exists"""

        self.brand_entry.insert(0, vehicle.get("brand", ""))
        self.model_entry.insert(0, vehicle.get("model", ""))
        self.year_entry.insert(0, str(vehicle.get("year", "")))
        self.registration_no_entry.insert(0, vehicle.get("registration_no", ""))
        self.color_entry.insert(0, vehicle.get("color", ""))
        self.action_btn.configure(text="Update")

    def handle_submit(self):
        vehicle_data = {
            "driver_id": config.loggedInUser['_id'],
            "brand": self.brand_entry.get(),
            "model": self.model_entry.get(),
            "year": int(self.year_entry.get()),
            "registration_no": self.registration_no_entry.get(),
            "color": self.color_entry.get()
        }

        try:
            vehicle_service = VehicleService()
            if self.vehicle_data:
                # Update existing vehicle
                vehicle_id = self.vehicle_data["_id"]
                vehicle_service.update_vehicle(vehicle_id, vehicle_data)
                self.status_label.configure(
                    text=f"Vehicle Updated (ID: {vehicle_id})", text_color="green"
                )
            else:
                # Insert new vehicle
                vehicle_id = vehicle_service.insert_vehicle(vehicle_data)
                self.status_label.configure(
                    text=f"Vehicle Created for {config.loggedInUser['_id']}. ID: {vehicle_id}", text_color="green"
                )
            
            self.manager.show_screen('view_vehicles')

        except Exception as e:
            print(e)
            self.status_label.configure(text=f"❌ {str(e)}", text_color="red")

    def go_back(self):
        if self.vehicle_data:
            self.manager.show_screen('view_vehicles')
        else:
            self.manager.show_screen('driver_dashboard')
