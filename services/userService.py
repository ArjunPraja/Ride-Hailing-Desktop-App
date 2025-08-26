from models.userModel import UserModel
class UserService:

    def list_users(self):
        pass

    def get_user(self, user_id):
        pass

    def insert_user(self, user_data):
        try:
            required_fields = ["name", "email", "phone_no", "role", "password"]
            if not all(user_data.get(f) for f in required_fields):
                raise ValueError("All required fields must be provided")
            
            new_user = UserModel(**user_data)
            return new_user.save() # returns _id of the new user
        except Exception as e:
            raise e

    def udpate_user(self, user_id, usr_data):
        pass

    def delete_user(self, user_id):
        pass

    def authenticate_user(self, email, password):
        try:
            user = UserModel.find_one({"email": email, "password": password})
            if user:
                return user.to_dict()
            return None
        except Exception as e:
            raise e