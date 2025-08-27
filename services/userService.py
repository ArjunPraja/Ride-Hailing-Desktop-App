from models.userModel import UserModel
import random, smtplib
from email.mime.text import MIMEText
from config import config_var as config
from datetime import datetime, timedelta

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
    
    def generate_and_send_otp(self, email):
        """Generate OTP, store temporarily, and send to user email"""
        otp = str(random.randint(100000, 999999))
        expiry = datetime.now() + timedelta(minutes=5)

        config.active_otps[email] = {"otp": otp, "expiry": expiry}
        sender_email = "rideappproj@gmail.com"   # the Gmail you made
        sender_pass = "axuvlrqbpxuxaqmx"
        # Send OTP email
        msg = MIMEText(f"Your OTP is: {otp}\nValid for 5 minutes.")
        msg["Subject"] = "Your Login OTP"
        msg["From"] = "rideappproj@gmail.com"
        msg["To"] = email

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, sender_pass)  # Gmail app password
                server.sendmail(sender_email, [email], msg.as_string())
            return True
        except Exception as e:
            print("Error sending OTP:", e)
            return False

    def verify_otp(self, email, otp):
        """Check if OTP is valid and not expired"""
        otp_data = config.active_otps.get(email)
        if otp_data and otp_data["otp"] == otp and datetime.now() <= otp_data["expiry"]:
            return True
        return False

    def authenticate_user_with_otp(self, email, otp):
        """Login via OTP"""
        if self.verify_otp(email, otp):
            user = UserModel.find_one({"email": email})
            if user:
                return user.to_dict()
        return None
    