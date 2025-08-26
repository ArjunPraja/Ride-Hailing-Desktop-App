import customtkinter as ctk
    
class LandingPage(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager
        
        self.grid_rowconfigure(0, weight=1)  # top spacer
        self.grid_columnconfigure(0, weight=1)  # left spacer
        
        content_frame = ctk.CTkFrame(self, bg_color="transparent")
        content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        content_frame.grid_rowconfigure((0,4) , weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Inside content
        label = ctk.CTkLabel(content_frame, text="Welcome to the Ride Hailing App", font=("Arial", 30))
        label.grid(row=1, column=0, pady=40, sticky="n")

        login_btn = ctk.CTkButton(content_frame, text="Login", command=lambda: manager.show_screen("login") if manager else None)
        login_btn.grid(row=2, column=0, pady=10)

        register_btn = ctk.CTkButton(content_frame, text="Register", command=lambda: manager.show_screen("signup") if manager else None)
        register_btn.grid(row=3, column=0, pady=10)