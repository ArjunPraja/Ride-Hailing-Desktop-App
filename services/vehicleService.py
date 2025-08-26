from models.vehicleModel import VehicleModel
class VehicleService:

    def list_vehicles(self):
        return VehicleModel.list_all_data()

    def get_vehicle(self, vehicle_id):
        pass

    def insert_vehicle(self, vehicle_data):
        try:

            required_fields = ["driver_id", "brand", "model", "year", "registration_no", "color"]
            if not all(vehicle_data.get(f) for f in required_fields):
                raise ValueError("All fields (driver_id, brand, model, year, registration_no, color) are required.")

            print(vehicle_data)
            new_vehicle = VehicleModel(**vehicle_data)
            return new_vehicle.save() # returns _id of the new vehicle
        except Exception as e:
            raise e

    def update_vehicle(self, vehicle_id, vehicle_data):
        try:
            result = VehicleModel.update({"_id":vehicle_id}, vehicle_data)
            return result
        except Exception as e:
            raise e

    def delete_vehicle(self, vehicle_id):
        pass