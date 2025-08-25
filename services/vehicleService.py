from models.vehicleModel import VehicleModel
class VehicleService:

    def list_vehicles(self):
        pass

    def get_vehicle(self, vehicle_id):
        pass

    def insert_vehicle(self, vehicle_data):
        try:
            driver_id = vehicle_data.get("driver_id")
            brand = vehicle_data.get("brand")
            model = vehicle_data.get("model")
            year = vehicle_data.get("year")
            registration_no = vehicle_data.get("registration_no")
            color = vehicle_data.get("color")

            if not all([driver_id, brand, model, year, registration_no, color]):
                raise ValueError("All fields (driver_id, brand, model, year, registration_no, color) are required.")

            new_vehicle = VehicleModel(driver_id, brand, model, year, registration_no, color, **vehicle_data)
            return new_vehicle.save() # returns _id of the new vehicle
        except Exception as e:
            raise e

    def update_vehicle(self, vehicle_id, vehicle_date):
        pass

    def delete_vehicle(self, vehicle_id):
        pass