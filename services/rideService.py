from models.rideModel import RideModel
from bson import ObjectId
class RideService:

    def list_rides(self, role, user_id):
        """List all rides for a given user (rider or driver)."""
        pipeline = []
        if role == "rider":
            pipeline = [{"$match": {"rider_id": user_id}}]
        elif role == "driver":
            pipeline = [{"$match": {"driver_id": user_id}}]

        return RideModel.list_all_data(pipeline)

    def get_ride(self, ride_id, user_role=None, user_id=None):
        """Fetch a single ride by ID with optional role-based filtering."""
        try:
            query = {"_id": ObjectId(ride_id)}
            if user_role == "rider":
                query["rider_id"] = user_id
            elif user_role == "driver":
                query["driver_id"] = user_id

            ride_obj = RideModel.find_one(query)
            return ride_obj.to_dict() if ride_obj else None
        except Exception as e:
            raise e

    def insert_ride(self, ride_data):
        try:
            rider_id = ride_data.get("rider_id")
            pickup_location = ride_data.get("pickup_location")
            drop_location = ride_data.get("drop_location")
            fare = ride_data.get("fare")
            status = ride_data.get("status")

            if not all([rider_id, pickup_location, drop_location, fare, status]):
                raise ValueError("Missing required ride data fields.")
            
            new_ride = RideModel(**ride_data)
            return new_ride.save() # return the ride _id
        except Exception as e:
            raise e

    def update_ride(self, ride_id, ride_data):
        try:
            return RideModel.update({"_id": ObjectId(ride_id)}, ride_data)
        except Exception as e:
            raise e

    def delete_ride(self, ride_id):
        pass