import customtkinter as ctk
import config.config_var as config
from services.vehicleService import VehicleService

class VehicleForm(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager

        self.grid_rowconfigure(0, weight=1)  # top spacer
        self.grid_columnconfigure(0, weight=1)  # left spacer

        # Main content frame
        self.content_frame = ctk.CTkFrame(self, bg_color="transparent")
        self.content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_rowconfigure((0,10), weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Header
        label = ctk.CTkLabel(self.content_frame, text="Register Vehicle", font=("Arial", 40))
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

        # Register button
        register_btn = ctk.CTkButton(self.content_frame, text="Register", command=self.handle_register, width=100, height=40, corner_radius=10, font=("Arial", 20))
        register_btn.grid(row=7, column=0, pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(self.content_frame, text="", font=("Arial", 12))
        self.status_label.grid(row=8, column=0, pady=5)

    def handle_register(self):
        # Collect data from entries
        vehicle_data = {
            "driver_id" : config.loggedInUser['_id'],
            "brand": self.brand_entry.get(),
            "model": self.model_entry.get(),
            "year": int(self.year_entry.get()),
            "registration_no": self.registration_no_entry.get(),
            "color": self.color_entry.get()
        }

        try:
            
            vehicle_service = VehicleService()
            vehicle_id = vehicle_service.insert_vehicle(vehicle_data)

            print(config.loggedInUser)
            if vehicle_id :
                self.status_label.configure(
                    text=f"Vehicle Crated for {config.loggedInUser['_id']}. ID: {vehicle_id}", text_color="green"
                )
            self.manager.show_screen('view_vehicles')

        except Exception as e:
            print(e)
            self.status_label.configure(text=f"❌ {str(e)}", text_color="red")
