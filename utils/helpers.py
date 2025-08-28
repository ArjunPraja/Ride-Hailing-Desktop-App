
import customtkinter as ctk

"""Recursively find all CTkEntry widgets inside a frame."""
def get_all_entries(frame):
    entries = []
    for child in frame.winfo_children():
        if isinstance(child, ctk.CTkEntry):
            entries.append(child)
        else:
            entries.extend(get_all_entries(child))
    return entries
