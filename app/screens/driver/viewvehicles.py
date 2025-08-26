import customtkinter as ctk
from app.screens.driver.vehicleform import VehicleForm
from services.vehicleService import VehicleService
import config.config_var as config

class ViewVehicle(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.content_frame = ctk.CTkFrame(self, bg_color="transparent")
        self.content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure((0,1), weight=1)

        header = ctk.CTkLabel(self.content_frame, text="My Vehicles", font=("Arial", 30))
        header.grid(row=0, column=0, columnspan=2, pady=(10,20))

        load_btn = ctk.CTkButton(
            self.content_frame, 
            text="Reload Vehicles", 
            command=self.load_vehicles
        )
        load_btn.grid(row=1, column=0, sticky="ew", padx=10)

        load_btn = ctk.CTkButton(
            self.content_frame, 
            text="Create Vehicle", 
            command=self.open_create_form
        )
        load_btn.grid(row=1, column=1, sticky="ew", padx=10)

        #  Frame for table
        self.list_frame = ctk.CTkFrame(self.content_frame)
        self.list_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        self.list_frame.grid_columnconfigure((0,1,2,3,4,5), weight=1)

    def load_vehicles(self):
        # Clear previous list
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        vehicle_service = VehicleService()
        vehicles = vehicle_service.list_vehicles()  # return list of dicts

        # ---- Table Header ----
        headers = ["Brand", "Model", "Year", "Registration No", "Color", "Action"]
        for col, text in enumerate(headers):
            label = ctk.CTkLabel(self.list_frame, text=text, font=("Arial", 14, "bold"))
            label.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

        if not vehicles:
            label = ctk.CTkLabel(self.list_frame, text="No vehicles found.")
            label.grid(row=1, column=0, columnspan=6, pady=10)
            return

        # ---- Table Rows ----
        for i, vehicle in enumerate(vehicles, start=1):
            if config.loggedInUser and config.loggedInUser["_id"] and str(vehicle['driver_id']) == str(config.loggedInUser["_id"]): 
                ctk.CTkLabel(self.list_frame, text=vehicle['brand']).grid(row=i, column=0, padx=10, pady=5, sticky="nsew")
                ctk.CTkLabel(self.list_frame, text=vehicle['model']).grid(row=i, column=1, padx=10, pady=5, sticky="nsew")
                ctk.CTkLabel(self.list_frame, text=vehicle['year']).grid(row=i, column=2, padx=10, pady=5, sticky="nsew")
                ctk.CTkLabel(self.list_frame, text=vehicle['registration_no']).grid(row=i, column=3, padx=10, pady=5, sticky="nsew")
                ctk.CTkLabel(self.list_frame, text=vehicle['color']).grid(row=i, column=4, padx=10, pady=5, sticky="nsew")

                update_btn = ctk.CTkButton(
                    self.list_frame, text="Update", width=100,
                    command=lambda v=vehicle: self.open_update_form(v)
                )
                update_btn.grid(row=i, column=5, padx=10, pady=5)

    def open_create_form(self):
        self.manager.show_screen('vehicle_form')

    def open_update_form(self, vehicle):
        self.manager.show_screen('vehicle_form', vehicle_data=vehicle)