import customtkinter as ctk
from services.rideService import RideService
import config.config_var as Config
from datetime import datetime

class MyRatingsDriver(ctk.CTkFrame):
    def __init__(self, parent, manager=None):
        super().__init__(parent)
        self.manager = manager
        self.ride_service = RideService()

        # Header
        header_frame = ctk.CTkFrame(self, height=60, fg_color="#1f6aa5")
        header_frame.pack(fill="x")
        header_label = ctk.CTkLabel(
            header_frame,
            text="My Ratings",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        header_label.pack(pady=15)

       # Back & Reload Button Frame
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        # Back Button
        back_btn = ctk.CTkButton(
            btn_frame,
            text="⬅ Back",
            width=120,
            command=self.go_back
        )
        back_btn.pack(side="left")

        # Reload Button
        reload_btn = ctk.CTkButton(
            btn_frame,
            text="Reload",
            width=120,
            fg_color="#1f6aa5",
            hover_color="#145a86",
            command=self.load_ratings
        )
        reload_btn.pack(side="right")

        # Average rating label
        self.avg_rating_label = ctk.CTkLabel(self, text="Average Rating: N/A", font=ctk.CTkFont(size=16, weight="bold"))
        self.avg_rating_label.pack(pady=5)

        # Scrollable frame for ride rating tiles
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=700, height=500)
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def go_back(self):
        if self.manager:
            self.manager.show_screen("driver_dashboard")

    def load_ratings(self):
        # Clear previous tiles
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        driver_id = Config.loggedInUser.get("_id")
        rides = self.ride_service.list_rides("driver", driver_id)

        total_score = 0
        count = 0

        if not rides:
            ctk.CTkLabel(self.scrollable_frame, text="No rides or ratings found.", text_color="red").pack(pady=10)
            self.avg_rating_label.configure(text="Average Rating: N/A")
            return

        for ride in rides:
            rating = ride.get("ratings")  # Single rating object
            if rating:
                total_score += rating.get("score", 0)
                count += 1

            # Determine tile color based on rating score (pastel theme)
            if rating:
                score = rating.get("score", 0)
                if score >= 4:
                    tile_color = "#C8FACC"  # Soft green
                elif score >= 3:
                    tile_color = "#FFF8B5"  # Soft yellow
                else:
                    tile_color = "#FECACA"  # Soft red/pink
            else:
                tile_color = "#f0f0f0"  # Default light gray for no rating

            # Tile frame
            tile = ctk.CTkFrame(self.scrollable_frame, corner_radius=12, fg_color=tile_color, border_width=1, border_color="#cccccc")
            tile.pack(fill="x", pady=10, padx=10)

            ride_date_str = ride.get("ride_date")
            if isinstance(ride_date_str, datetime):
                ride_date_str = ride_date_str.strftime("%d %b %Y, %I:%M %p")
            else:
                ride_date_str = str(ride_date_str)

            # Ride details
            details = (
                f"Ride ID: {ride.get('_id')}\n"
                f"Pickup: {ride.get('pickup_location', 'N/A')}\n"
                f"Drop: {ride.get('drop_location', 'N/A')}\n"
                f"Date: {ride_date_str}\n"
            )
            ctk.CTkLabel(tile, text=details, justify="left", anchor="w", font=ctk.CTkFont(size=14)).pack(side="top", padx=15, pady=(10,0), fill="x")

            if rating:
                comment = rating.get("comment", "")
                rating_text = f"Rating: {rating.get('score', 'N/A')}/5"
                if comment:
                    rating_text += f"\nComment: {comment}"
                ctk.CTkLabel(tile, text=rating_text, anchor="w", justify="left", text_color="#1f6aa5").pack(side="top", padx=15, pady=5, fill="x")
            else:
                ctk.CTkLabel(tile, text="No rating yet", anchor="w", justify="left", text_color="gray").pack(side="top", padx=15, pady=5, fill="x")

        # Update average rating
        avg_rating = round(total_score / count, 2) if count > 0 else "N/A"
        self.avg_rating_label.configure(text=f"Average Rating: {avg_rating}/5")