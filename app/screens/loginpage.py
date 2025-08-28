import customtkinter as ctk
import config.config_var as config
from services.userService import UserService
from app.utils.helpers import get_all_entries

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager
        self.user_service = UserService()
        self.current_mode = "password" #default mode

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

        self.otp_entry = ctk.CTkEntry(content_frame, placeholder_text="Enter OTP", width=250, height=40, corner_radius=8)
        self.otp_entry.grid(row=3, column=0, padx=200, pady=10, sticky="ew")
        self.otp_entry.grid_remove()

        switch_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        switch_frame.grid(row=4, column=0, pady=10)

        # self.pwd_mode_btn = ctk.CTkButton(switch_frame, text="🔑 Login with Password", command=self.show_password_mode, width=160, height=35, corner_radius=8)
        # self.pwd_mode_btn.grid(row=0, column=0, padx=5)

        self.otp_mode_btn = ctk.CTkButton(switch_frame, text="📩 Login with OTP", command=self.show_otp_mode, width=160, height=35, corner_radius=8)
        self.otp_mode_btn.grid(row=0, column=1, padx=5)
        
        self.login_btn = ctk.CTkButton(content_frame, text="Login", command=self.handle_login, width=100, height=40, corner_radius=10, font=("Arial", 20))
        self.login_btn.grid(row=5, column=0, pady=10, padx=200, sticky="ew")

        self.send_otp_btn = ctk.CTkButton(content_frame, text="Send OTP", command=self.send_otp, width=100, height=35, corner_radius=8)
        self.send_otp_btn.grid(row=6, column=0, pady=5)
        self.send_otp_btn.grid_remove()

        # login_btn = ctk.CTkButton(content_frame, text="Login", command=self.handle_login, width=100, height=40, corner_radius=10, font=("Arial", 20))
        # login_btn.grid(row=4, column=0, pady=10,padx=200, sticky="ew")

        # self.otp_entry = ctk.CTkEntry(content_frame, placeholder_text="Enter OTP",
        #                               width=250, height=40, corner_radius=8)
        # self.otp_entry.grid(row=5, column=0, padx=200, pady=10, sticky="ew")

        # otp_btn = ctk.CTkButton(content_frame, text="Send OTP",
        #                         command=self.send_otp, width=100, height=35,
        #                         corner_radius=8, font=("Arial", 14))
        # otp_btn.grid(row=6, column=0, pady=5, padx=200, sticky="ew")

        # otp_login_btn = ctk.CTkButton(content_frame, text="Login with OTP",
        #                               command=self.handle_login_with_otp, width=100, height=35,
        #                               corner_radius=8, font=("Arial", 14))
        # otp_login_btn.grid(row=7, column=0, pady=5, padx=200, sticky="ew")

        back_btn = ctk.CTkButton(content_frame, text="⬅ Back", width=40, height=40, corner_radius=10, command=lambda: self.manager.show_screen("landing") if self.manager else None)
        back_btn.grid(row=7, column=0,  pady=10,padx=200)

        # Status label
        self.status_label = ctk.CTkLabel(content_frame, text="", font=("Arial", 12))
        self.status_label.grid(row=8, column=0, pady=5)

    def show_password_mode(self):
        self.current_mode = "password"
        self.password_entry.grid()
        self.otp_entry.grid_remove()
        self.send_otp_btn.grid_remove()
        self.status_label.configure(text="")

    def show_otp_mode(self):
        self.current_mode = "otp"
        self.password_entry.grid_remove()
        self.otp_entry.grid()
        self.send_otp_btn.grid()
        self.status_label.configure(text="")
       
    # def handle_login(self):
    #     email = self.email_entry.get()
    #     password = self.password_entry.get()

    #     if email and password:
    #         user_service = UserService()
    #         user = user_service.authenticate_user(email, password)
    #         if user:

    #             config.loggedInUser = user
    #             self.status_label.configure(text="Login Successful!", text_color="green")
    #             self.show_popup(f"🎉 Login SuccessFull {user['name']}, {user['role']}", "green")
    #             # print(config.loggedInUser)

    #             self.navigate_dashboard()
    #             # if self.manager: 
    #             #     if config.loggedInUser['role'] == 'rider':
    #             #         self.manager.show_screen("rider_dashboard")
    #             #     elif config.loggedInUser['role'] == 'driver':
    #             #         self.manager.show_screen("driver_dashboard")
    #             #     # elif Config.loggedInUser['role'] == 'admin':
    #             #     #     self.manager.show_screen("rider_dashboard")
    #         else:
    #             self.status_label.configure(text="Invalid credentials", text_color="red")
    #     else:
    #         self.status_label.configure(text="Invalid credentials", text_color="red")

    def send_otp(self):
        email = self.email_entry.get()
        if not email:
            self.status_label.configure(text="Please enter your email first", text_color="red")
            return

        sent = self.user_service.generate_and_send_otp(email)
        if sent:
            self.status_label.configure(text="✅ OTP sent to your email", text_color="green")
        else:
            self.status_label.configure(text="❌ Failed to send OTP", text_color="red")

    # def handle_login_with_otp(self):
    #     email = self.email_entry.get()
    #     otp = self.otp_entry.get()

    #     if email and otp:
    #         user_service = UserService()
    #         user = user_service.authenticate_user_with_otp(email, otp)
    #         if user:
    #             config.loggedInUser = user
    #             self.status_label.configure(text="Login Successful via OTP!", text_color="green")
    #             self.show_popup(f"🎉 Welcome {user['name']} ({user['role']})", "green")
    #             self.navigate_dashboard()
    #         else:
    #             self.status_label.configure(text="Invalid or expired OTP", text_color="red")
    #     else:
    #         self.status_label.configure(text="Please enter email & OTP", text_color="red")
    def handle_login(self):
        email = self.email_entry.get()

        if self.current_mode == "password":
            password = self.password_entry.get()
            if email and password:
                user = self.user_service.authenticate_user(email, password)
                if user:
                    config.loggedInUser = user
                    self.status_label.configure(text="Login Successful!", text_color="green")
                    self.show_dashboard(user)
                else:
                    self.status_label.configure(text="Invalid credentials", text_color="red")
            else:
                self.status_label.configure(text="Enter email and password", text_color="red")

        elif self.current_mode == "otp":
            otp = self.otp_entry.get()
            if email and otp:
                if self.user_service.verify_otp(email, otp):
                    user = self.user_service.authenticate_user_with_otp(email,otp)
                    if user:
                        config.loggedInUser = user
                        self.status_label.configure(text="OTP Login Successful!", text_color="green")
                        self.show_dashboard(user)
                    else:
                        self.status_label.configure(text="User not found", text_color="red")
                else:
                    self.status_label.configure(text="Invalid OTP", text_color="red")
            else:
                self.status_label.configure(text="Enter email and OTP", text_color="red")
    # -----------------------
    def show_dashboard(self):
        if self.manager:
            if config.loggedInUser['role'] == 'rider':
                self.manager.show_screen("rider_dashboard")
            elif config.loggedInUser['role'] == 'driver':
                self.manager.show_screen("driver_dashboard")

    def show_dashboard(self, user):
        if self.manager:
            if user['role'] == 'rider':
                self.manager.show_screen("rider_dashboard")
            elif user['role'] == 'driver':
                self.manager.show_screen("driver_dashboard")

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
        entries = get_all_entries(self)

        for e in entries:
            e.delete(0, "end")

        self.status_label.configure(text="")

        # Force focus away 
        self.focus_set()

        for e in entries:
            try:
                e.event_generate("<FocusOut>")
            except Exception:
                pass
            if hasattr(e, "_draw_placeholder"):
                try:
                    e._draw_placeholder()
                except Exception:
                    pass
        
