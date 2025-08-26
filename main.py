# from config.database import db_config

# db = db_config.connect()

import customtkinter as ctk
from app.screen_manager import ScreenManager
from app.screens.landing_page import LandingPage
from app.screens.loginpage import LoginPage
from app.screens.registerpage import RegisterPage

def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Ride Hailing App")
    app.geometry("800x600")
    app.resizable(False, False)

    manager = ScreenManager(app)
    manager.add_screen("landing", LandingPage)
    manager.add_screen("login", LoginPage)  # Assuming LoginPage is defined elsewhere
    manager.add_screen("signup", RegisterPage)  # Assuming SignupPage is defined elsewhere

    manager.show_screen("landing")

    app.mainloop()

if __name__ == "__main__":
    main()