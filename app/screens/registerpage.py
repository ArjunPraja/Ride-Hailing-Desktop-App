import customtkinter as ctk

class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager

        self.grid_rowconfigure(0, weight=1)  # top spacer
        self.grid_columnconfigure(0, weight=1)  # left spacer

        content_frame = ctk.CTkFrame(self, bg_color="transparent")
        content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        content_frame.grid_rowconfigure((0,9), weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(content_frame, text="Register", font=("Arial", 40))
        label.grid(row=1, column=0, pady=(20,30), sticky="n")

        self.name_entry = ctk.CTkEntry(content_frame, placeholder_text="Enter your name", width=250, height=40, corner_radius=8)
        self.name_entry.grid(row=2, column=0, padx=200, pady=10, sticky="ew")

        self.email_entry = ctk.CTkEntry(content_frame, placeholder_text="Enter your email", width=250, height=40, corner_radius=8)
        self.email_entry.grid(row=3, column=0, padx=200, pady=10, sticky="ew")

        self.phone_no_entry = ctk.CTkEntry(content_frame, placeholder_text="Enter your phone number", width=250, height=40, corner_radius=8)
        self.phone_no_entry.grid(row=4, column=0, padx=200, pady=10, sticky="ew")

        # Role dropdown instead of entry
        self.role_dropdown = ctk.CTkOptionMenu(
            content_frame, 
            values=["Rider", "Driver"],
            width=250, 
            height=40, 
            corner_radius=8,
            font=("Arial", 14)
        )
        self.role_dropdown.grid(row=5, column=0, padx=200, pady=10, sticky="ew")
        self.role_dropdown.set("Select Role")  # default text
        self.password_entry = ctk.CTkEntry(content_frame, placeholder_text="Enter your password", show="*", width=250, height=40, corner_radius=8)
        self.password_entry.grid(row=6, column=0, padx=200, pady=10, sticky="ew")

        self.confirm_password_entry = ctk.CTkEntry(content_frame, placeholder_text="Confirm your password", show="*", width=250, height=40, corner_radius=8)
        self.confirm_password_entry.grid(row=7, column=0, padx=200, pady=10, sticky="ew")

        register_btn = ctk.CTkButton(content_frame, text="Register", command=self.handle_register, width=100, height=40, corner_radius=10, font=("Arial", 20))
        register_btn.grid(row=8, column=0, pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(content_frame, text="", font=("Arial", 12))
        self.status_label.grid(row=9, column=0, pady=5)

    def handle_register(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        role = self.role_dropdown.get()

        # Dummy validation (replace with DB/backend later)
        if password != confirm_password:
            self.status_label.configure(text="Passwords do not match", text_color="red")
        elif role == "Select Role":
            self.status_label.configure(text="Please select a role", text_color="red")
        else:
            self.status_label.configure(text=f"Registered as {role}", text_color="green")