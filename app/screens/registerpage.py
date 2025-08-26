import customtkinter as ctk
from models.userModel import UserModel
from services.userService import UserService

class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager

        self.grid_rowconfigure(0, weight=1)  # top spacer
        self.grid_columnconfigure(0, weight=1)  # left spacer

        self.content_frame = ctk.CTkFrame(self, bg_color="transparent")
        self.content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_rowconfigure((0,10), weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(self.content_frame, text="Register", font=("Arial", 40))
        label.grid(row=1, column=0, pady=(20,30), sticky="n")

        self.name_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Enter your name", width=250, height=40, corner_radius=8)
        self.name_entry.grid(row=2, column=0, padx=200, pady=10, sticky="ew")

        self.email_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Enter your email", width=250, height=40, corner_radius=8)
        self.email_entry.grid(row=3, column=0, padx=200, pady=10, sticky="ew")

        self.phone_no_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Enter your phone number", width=250, height=40, corner_radius=8)
        self.phone_no_entry.grid(row=4, column=0, padx=200, pady=10, sticky="ew")

        # Role dropdown instead of entry
        self.role_dropdown = ctk.CTkOptionMenu(
            self.content_frame, 
            values=["rider", "driver"],
            width=250, 
            height=40, 
            corner_radius=8,
            font=("Arial", 14),
            command=self.role_selected
        )
        self.role_dropdown.grid(row=5, column=0, padx=200, pady=10, sticky="ew")
        self.role_dropdown.set("Select Role")  # default text

        # Placeholder for license entry (hidden initially)
        self.license_entry = None

        # if self.role_dropdown.get() == "driver":
        #     self.license_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Enter your license number", width=250, height=40, corner_radius=8)
        #     self.license_entry.grid(row=6, column=0, padx=200, pady=10, sticky="ew")

        self.password_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Enter your password", show="*", width=250, height=40, corner_radius=8)
        self.password_entry.grid(row=7, column=0, padx=200, pady=10, sticky="ew")

        self.confirm_password_entry = ctk.CTkEntry(self.content_frame, placeholder_text="Confirm your password", show="*", width=250, height=40, corner_radius=8)
        self.confirm_password_entry.grid(row=8, column=0, padx=200, pady=10, sticky="ew")

        register_btn = ctk.CTkButton(self.content_frame, text="Register", command=self.handle_register, width=100, height=40, corner_radius=10, font=("Arial", 20))
        register_btn.grid(row=9, column=0, pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(self.content_frame, text="", font=("Arial", 12))
        self.status_label.grid(row=10, column=0, pady=5)

    # Dynamically show/hide license entry
    def role_selected(self, value):
        if value.lower() == "driver":
            if not self.license_entry:
                self.license_entry = ctk.CTkEntry(
                    self.content_frame,
                    placeholder_text="Enter your license number",
                    width=250,
                    height=40,
                    corner_radius=8
                )
                self.license_entry.grid(row=6, column=0, padx=200, pady=10, sticky="ew")
            else:
                self.license_entry.grid()
        else:
            if self.license_entry:
                self.license_entry.grid_remove()

    def handle_register(self):
        print("Register Called")
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone_no = self.phone_no_entry.get()
        role = self.role_dropdown.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Get license number if it exists (for driver role)
        license_no = getattr(self, 'license_entry', None)
        license_no_value = license_no.get() if license_no else None

        if password != confirm_password:
            self.status_label.configure(text="Passwords do not match", text_color="red")
            return
        elif role == "Select Role":
            self.status_label.configure(text="Please select a role", text_color="red")
            return

        # Prepare user data dictionary for service
        user_data = {
            "name": name,
            "email": email,
            "phone_no": phone_no,
            "role": role,
            "password": password,
        }

        # Add extra fields if present
        if license_no_value:
            user_data["license_no"] = license_no_value

        try:
            # Call your UserService
            user_service = UserService()
            user_id = user_service.insert_user(user_data)  # pass the dictionary

            self.status_label.configure(
                text=f"✅ Registered as {role}. ID: {user_id}", text_color="green"
            )
        except Exception as e:
            print(e)
            self.status_label.configure(text=f"❌ {str(e)}", text_color="red")