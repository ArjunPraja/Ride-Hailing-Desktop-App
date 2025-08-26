from models.rideModel import RideModel
class RideService:

    def list_rides(self):
        pass

    def get_ride(self, ride_id):
        pass

    def insert_ride(self, ride_data):
        try:
            rider_id = ride_data.get("rider_id")
            pickup_location = ride_data.get("pickup_location")
            drop_location = ride_data.get("drop_location")
            fare = ride_data.get("fare")
            status = ride_data.get("status")

            if not all([rider_id, pickup_location, drop_location, fare, status]):
                raise ValueError("Missing required ride data fields.")
            
            new_ride = RideModel(rider_id = rider_id, pickup_location=pickup_location, drop_location = drop_location, fare = fare, status = status, **ride_data)
            return new_ride.save() # return the ride _id
        except Exception as e:
            raise e

    def update_ride(self, ride_id, ride_data):
        pass

    def delete_ride(self, ride_id):
        pass