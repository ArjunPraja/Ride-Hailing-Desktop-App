import customtkinter as ctk
import config.config_var as config
from services.userService import UserService

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager

        self.grid_rowconfigure(0, weight=1)  # top spacer
        self.grid_columnconfigure(0, weight=1)  # left spacer

        content_frame = ctk.CTkFrame(self, bg_color="transparent")
        content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        content_frame.grid_rowconfigure((0,5), weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(content_frame, text="Login", font=("Arial", 40))
        label.grid(row=1, column=0, pady=(20,30), sticky="n")

        self.email_entry = ctk.CTkEntry(content_frame, placeholder_text="Enter your email", width=250, height=40, corner_radius=8)
        self.email_entry.grid(row=2, column=0, padx=200, pady=10, sticky="ew")

        self.password_entry = ctk.CTkEntry(content_frame, placeholder_text="Enter your password", show="*", width=250, height=40, corner_radius=8)
        self.password_entry.grid(row=3, column=0, padx=200, pady=10, sticky="ew")

        login_btn = ctk.CTkButton(content_frame, text="Login", command=self.handle_login, width=100, height=40, corner_radius=10, font=("Arial", 20))
        login_btn.grid(row=4, column=0, pady=10,padx=200, sticky="ew")

        back_btn = ctk.CTkButton(
            self,
            text="⬅",
            command=lambda: manager.show_screen("landing") if manager else None,
            width=100,
            height=35
        )
        # Use grid, row=99 makes it go to bottom, col=0 keeps it left
        back_btn.grid(row=99, column=0, sticky="w", padx=10, pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(content_frame, text="", font=("Arial", 12))
        self.status_label.grid(row=6, column=0, pady=5)

    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email and password:
            user_service = UserService()
            user = user_service.authenticate_user(email, password)
            if user:

                config.loggedInUser = user
                self.status_label.configure(text="Login Successful!", text_color="green")
                self.show_popup(f"🎉 Login SuccessFull {user['name']}, {user['role']}", "green")
                # print(config.loggedInUser)
                if self.manager: 
                    if config.loggedInUser['role'] == 'rider':
                        self.manager.show_screen("rider_dashboard")
                    elif config.loggedInUser['role'] == 'driver':
                        self.manager.show_screen("driver_dashboard")
                    # elif Config.loggedInUser['role'] == 'admin':
                    #     self.manager.show_screen("rider_dashboard")
            else:
                self.status_label.configure(text="Invalid credentials", text_color="red")
        else:
            self.status_label.configure(text="Invalid credentials", text_color="red")

    def show_popup(self, message, color="green"):
        popup = ctk.CTkToplevel(self)
        popup.geometry("400x180")
        popup.title("Notification")
        popup.grab_set()  # Make modal

        popup_label = ctk.CTkLabel(
            popup, 
            text=message, 
            font=("Arial", 18, "bold"), 
            text_color=color,
            wraplength=350,
            justify="center"
        )
        popup_label.pack(expand=True, pady=30, padx=20)

        ok_button = ctk.CTkButton(
            popup, 
            text="OK ✅", 
            width=100,
            height=40,
            font=("Arial", 14, "bold"),
            corner_radius=12,
            command=popup.destroy
        )
        ok_button.pack(pady=10)
    
    def reset_screen(self):
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.status_label.configure(text="")
        self.email_entry.update_idletasks()
        self.password_entry.update_idletasks()