import re
from models.baseModel import BaseModel

class UserModel(BaseModel):

    collection_name = 'users'

    def __init__(self, name, email, phone_no, role, password, **data):
        super().__init__(**data)
        self.name = name
        self.email = email
        self.phone_no = phone_no
        self.role = role
        self.password = password 

    def validate(self):
        errors = []

        # Name validation
        if not self.name or len(self.name.strip()) < 2:
            errors.append("Name must be at least 2 characters long.")

        # Email validation (basic regex)
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, self.email):
            errors.append("Invalid email format.")

        # Phone number validation (10 digits)
        phone_regex = r'^\d{10}$'
        if not re.match(phone_regex, self.phone_no):
            errors.append("Phone number must be 10 digits.")

        # Role validation (restrict to known roles)
        valid_roles = ["admin", "rider", "driver"]
        if self.role not in valid_roles:
            errors.append(f"Role must be one of ['rider', 'driver'].")

        # Password validation (min 8 chars, at least 1 number + 1 special char)
        pwd_regex = r'^(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$'
        if not re.match(pwd_regex, self.password):
            errors.append("Password must be at least 8 characters long, include a number and a special character.")

        if errors:
            raise ValueError({"validation_errors": errors})

        return True