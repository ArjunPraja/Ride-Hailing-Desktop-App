from models.baseModel import BaseModel
from datetime import datetime, timezone

class RideModel(BaseModel):

    collection_name = "rides"

    def __init__(self, rider_id, pickup_location, drop_location, fare, status,ratings=None, **data):
        super().__init__(**data)
        self.rider_id = rider_id
        self.pickup_location = pickup_location
        self.drop_location = drop_location
        self.fare = fare
        self.status = status
        self.ride_date = datetime.now(timezone.utc)
        self.ratings = ratings or []

    def validate(self):
        errors = []
        
        # rider_id validation: must be a valid ObjectId string
        from bson import ObjectId
        try:
             ObjectId(str(self.rider_id))
        except Exception:
             errors.append("Invalid rider_id.")

        # pickup_location and drop_location: should not be empty
        if not self.pickup_location or not self.pickup_location.strip():
            errors.append("Pickup location is required.")
        if not self.drop_location or not self.drop_location.strip():
            errors.append("Drop location is required.")

        # fare validation: must be a positive number
        if not isinstance(self.fare, (int, float)) or self.fare <= 0:
            errors.append("Fare must be a positive number.")

        # status validation: restrict to predefined statuses
        valid_statuses = ["requested", "accepted", "in_progress", "completed", "cancelled"]
        if self.status not in valid_statuses:
            errors.append(f"Status must be one of {valid_statuses}.")

        # ride_date: ensure it's a datetime object
        if not isinstance(self.ride_date, datetime):
            errors.append("ride_date must be a datetime object.")
        
        if not isinstance(self.ratings, list):
            errors.append("Ratings must be a list.")
        else:
            for rating in self.ratings:
                if not isinstance(rating, dict):
                    errors.append("Each rating must be an object {given_by, given_to, score, comment}.")
                else:
                    if "given_by" not in rating or "given_to" not in rating or "score" not in rating:
                        errors.append("Rating must contain 'given_by', 'given_to', and 'score'.")
                    elif not isinstance(rating["score"], int) or not (1 <= rating["score"] <= 5):
                        errors.append("Rating 'score' must be an integer between 1 and 5.")

        # raise error if any validation fails
        if errors:
            raise ValueError({"validation_errors": errors})

        return True
