from models.userModel import UserModel
class UserService:

    def list_users(self):
        pass

    def get_user(self, user_id):
        pass

    def insert_user(self, user_data):
        try:
            name = user_data.get('name')
            email = user_data.get('email')
            phone_no = user_data.get('phone_no')
            role = user_data.get('role')
            password = user_data.get('password')

            if not all([name, email, phone_no, role, password]):
                raise ValueError("All fields (name, email, phone_no, role, password) are required.")
            
            new_user = UserModel(name, email, phone_no, role, password, **user_data)
            return new_user.save() # returns _id of the new user
        except Exception as e:
            raise e

    def udpate_user(self, user_id, usr_data):
        pass

    def delete_user(self, user_id):
        pass