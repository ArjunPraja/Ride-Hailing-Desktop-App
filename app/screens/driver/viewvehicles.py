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
        self.content_frame.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(self.content_frame, text="My Vehicles", font=("Arial", 30))
        header.grid(row=0, column=0, pady=(10,20))

        # Container for vehicle list
        self.list_frame = ctk.CTkFrame(self.content_frame)
        self.list_frame.grid(row=1, column=0, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.load_vehicles()

    def load_vehicles(self):
        # Clear previous list
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        vehicle_service = VehicleService()
        vehicles = vehicle_service.list_vehicles()  # return list of dicts

        print(config.loggedInUser)
        if not vehicles:
            label = ctk.CTkLabel(self.list_frame, text="No vehicles found.")
            label.grid(row=0, column=0, pady=10)
            return

        for i, vehicle in enumerate(vehicles):
            if config.loggedInUser and config.loggedInUser._id and str(vehicle['driver_id']) == str(config.loggedInUser._id): 
                info_text = f"{vehicle['brand']} | {vehicle['model']} | {vehicle['year']} | {vehicle['registration_no']} | {vehicle['color']}"
                info_label = ctk.CTkLabel(self.list_frame, text=info_text, anchor="w")
                info_label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

                update_btn = ctk.CTkButton(self.list_frame, text="Update", width=100,
                                        command=lambda v=vehicle: self.open_update_form(v))
                update_btn.grid(row=i, column=1, padx=10, pady=5)

    def open_update_form(self, vehicle):
        # Open a VehicleForm pre-filled with vehicle data
        form = VehicleForm(self, manager=self.manager, vehicle=vehicle)  # pass vehicle to form
        form.grid(row=0, column=0, sticky="nsew")
        form.tkraise()  # bring it to front