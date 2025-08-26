import re
from models.baseModel import BaseModel
from datetime import datetime

class VehicleModel(BaseModel):

    collection_name =  'vehicles'

    def __init__(self, driver_id, brand, model, year, registration_no, color, **data):
        super().__init__(**data)
        self.driver_id = driver_id
        self.brand = brand
        self.model = model
        self.year = year
        self.registration_no = registration_no
        self.color = color

    def validate(self):
        errors = []

        # driver_id: must be a valid ObjectId string
        from bson import ObjectId
        try:
            ObjectId(str(self.driver_id))
        except Exception:
            errors.append("Invalid driver_id.")

        # brand, model, color: non-empty strings
        if not self.brand or not self.brand.strip():
            errors.append("Brand is required.")
        if not self.model or not self.model.strip():
            errors.append("Model is required.")
        if not self.color or not self.color.strip():
            errors.append("Color is required.")

        # year: reasonable range (e.g., 1980 <= year <= current year + 1)
        current_year = datetime.now().year
        if not isinstance(self.year, int) or not (1980 <= self.year <= current_year + 1):
            errors.append(f"Year must be between 1980 and {current_year + 1}.")

        # registration_no: non-empty, can also add regex for standard formats
        if not self.registration_no or not self.registration_no.strip():
            errors.append("Registration number is required.")
        else:
            reg_regex = r'^[A-Z0-9-]{5,15}$'  # basic alphanumeric + dash format
            if not re.match(reg_regex, self.registration_no.upper()):
                errors.append("Registration number format is invalid.")

        # raise error if any validation fails
        if errors:
            raise ValueError({"validation_errors": errors})

        return True
