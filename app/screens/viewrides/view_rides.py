import customtkinter as ctk
from tkinter import messagebox, simpledialog
import config.config_var as Config
from services.rideService import RideService

class ViewMyRidesPage(ctk.CTkFrame):
    def __init__(self, root, manager):
        super().__init__(root)
        self.manager = manager
        self.ride_service = RideService()

        # Title
        ctk.CTkLabel(self, text="My Rides", font=("Arial", 18, "bold")).pack(pady=15)

        # Scroll
        self.rides_frame = ctk.CTkScrollableFrame(self, corner_radius=12, width=400, height=300)
        self.rides_frame.pack(pady=15, padx=10, fill="both", expand=True)

        #Back
        back_btn = ctk.CTkButton(
            self,
            text="⬅",
            command=lambda: self.manager.show_screen("rider_dashboard"),
            width=100,
            height=35
        )
        back_btn.pack(pady=10, anchor="w", padx=10)


    def clear_rides(self):
        """Clear old ride widgets"""
        for widget in self.rides_frame.winfo_children():
            widget.destroy()

    #cancel ride
    def cancel_ride(self, ride_id):
        try:
            success = self.ride_service.update_ride(ride_id, {"status": "cancelled"})
            if success:
                messagebox.showinfo("Success", f"Ride {ride_id} cancelled.")
                self.fetch_my_rides() 
            else:
                messagebox.showerror("Error", f"Could not cancel ride {ride_id}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error cancelling ride: {e}")


    #rating
    def submit_rating(self, ride_id, score, comment):
        user = Config.loggedInUser
        ride = self.ride_service.get_ride(ride_id)
        driver_id = ride.get("driver_id", "")
        rating = {
            "given_by": str(user["_id"]),   
            "given_to": str("driver_id", ""),
            "score": int(score),
            "comment": comment.strip()
        }

        try:
            success = self.ride_service.add_rating(ride_id, rating)
            if success:
                messagebox.showinfo("Thank you!", f"You rated this ride {score}/5.")
                self.fetch_my_rides()
            else:
                messagebox.showinfo("Already Rated", "You have already rated this ride.")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving rating: {e}")


    #complete ride
    def complete_ride(self, ride_id):
        try:
            success = self.ride_service.update_ride(ride_id, {"status": "completed"})
            if success:
                messagebox.showinfo("Success", f"Ride {ride_id} marked as completed.")
                self.fetch_my_rides()  
            else:
                messagebox.showerror("Error", f"Could not complete ride {ride_id}.")
        except Exception as e:
            messagebox.showerror("Error", f"Error completing ride: {e}")


    def fetch_my_rides(self):
        self.clear_rides()

        if not Config.loggedInUser:
            messagebox.showwarning("Warning", "No user is logged in!")
            return

        user_id = Config.loggedInUser["_id"]
        role = Config.loggedInUser.get("role", "")

        try:
             rides = self.ride_service.list_rides(role, user_id)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching rides: {e}")
            return

        if not rides:
            ctk.CTkLabel(
                self.rides_frame,
                text="No rides found for your account",
                text_color="red"
            ).pack(pady=10)
            return

       #Each card
        for ride in rides:
            card = ctk.CTkFrame(self.rides_frame, corner_radius=10, fg_color="#f0e9e9")
            card.pack(fill="x", padx=10, pady=5)

            # Status color
            status = ride.get("status", "Unknown")
            color = "green" if status.lower() == "completed" else "orange" if status.lower() == "ongoing" else "red"

            # Labels inside card
            ctk.CTkLabel(card, text=f"Ride ID: {ride.get('_id')}", font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(card, text=f"Pickup: {ride.get('pickup_location', 'N/A')}", anchor="w").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Drop: {ride.get('drop_location', 'N/A')}", anchor="w").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Fare: ₹{ride.get('fare', 0)}", anchor="w").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Status: {status}", text_color=color, anchor="w").pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=f"Date: {ride.get('ride_date', 'N/A')}", anchor="w").pack(anchor="w", padx=10)
            
            ratings = ride.get("ratings", [])
            user_id = str(Config.loggedInUser["_id"])

            already_rated = any(r.get("given_by") == user_id for r in ratings)

            if status.lower() == "completed" and role == "rider":
                if already_rated:
                    # show user's rating
                    for r in ratings:
                        if r.get("given_by") == "rider":
                            ctk.CTkLabel(card, text=f"Your Rating: {r['score']}/5", anchor="w", text_color="blue").pack(anchor="w", padx=10, pady=(5,0))
                            if r.get("comment"):
                                ctk.CTkLabel(card, text=f"Comment: {r['comment']}", anchor="w").pack(anchor="w", padx=20)
                else:
                    # add rating UI
                    ctk.CTkLabel(card, text="Rate this ride:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(5,0))

                    score_var = ctk.StringVar(value="5")
                    score_dropdown = ctk.CTkOptionMenu(card, variable=score_var, values=["1", "2", "3", "4", "5"])
                    score_dropdown.pack(anchor="w", padx=10, pady=2)

                    comment_entry = ctk.CTkEntry(card, placeholder_text="Add a comment (optional)", width=300)
                    comment_entry.pack(anchor="w", padx=10, pady=2)

                    submit_btn = ctk.CTkButton(
                        card,
                        text="Submit Rating",
                        fg_color="blue",
                        hover_color="darkblue",
                        command=lambda ride_id=ride["_id"], sv=score_var, ce=comment_entry: self.submit_rating(ride_id, sv.get(), ce.get())
                    )
                    submit_btn.pack(anchor="e", padx=10, pady=5)

            if status.lower() in ["requested", "accepted", "ongoing"]:
                ctk.CTkButton(
                    card,
                    text="Cancel Ride",
                    command=lambda ride_id=ride["_id"]: self.cancel_ride(ride_id),
                    fg_color="red",
                    hover_color="darkred"
                ).pack(pady=5, padx=10, anchor="e")
            
            if status.lower() == "ongoing" and role == "driver":
                ctk.CTkButton(
                    card,
                    text="Complete Ride",
                    command=lambda ride_id=ride["_id"]: self.complete_ride(ride_id),
                    fg_color="green",
                    hover_color="darkgreen"
                ).pack(pady=5, padx=10, anchor="e")
            
            
