import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import DateEntry
import os
import sys
import json
from PIL import Image

# Configure paths and load the JSON configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, '../config')
data_path = os.path.join(CONFIG_DIR, 'data.json')  # Path for the JSON config
sys.path.insert(0, CONFIG_DIR)

from db_connection import db

# Load configuration from JSON
with open(data_path, 'r') as file:
    config_data = json.load(file)

# Font styles from JSON
FONT_H1 = (config_data["fonts"]["h1"][0], config_data["fonts"]["h1"][1], config_data["fonts"]["h1"][2])
FONT_H2 = (config_data["fonts"]["h2"][0], config_data["fonts"]["h2"][1], config_data["fonts"]["h2"][2])
FONT_H3 = (config_data["fonts"]["h3"][0], config_data["fonts"]["h3"][1], config_data["fonts"]["h3"][2])
FONT_H4 = (config_data["fonts"]["h4"][0], config_data["fonts"]["h4"][1], config_data["fonts"]["h4"][2])

# Departments and Roles from JSON
DEPARTMENTS = config_data["departments"]
ROLES = config_data["roles"]

# Color scheme
BACKGROUND_COLOR = "#1E1E1E"
FRAME_COLOR = "#2A2A2A"
TEXT_COLOR = "#FFFFFF"
ACCENT_COLOR = "#007ACC"
BUTTON_COLOR = "#3C3C3C"
BUTTON_HOVER_COLOR = "#4E4E4E"

class SupervisorConstraintsApp(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BACKGROUND_COLOR)
        self.master = master
        self.db = db
        self.supervisors = self.load_supervisors()
        self.create_widgets()
        self.pack(fill="both", expand=True, padx=20, pady=20)

    def load_supervisors(self):
        query = "SELECT id, name, rfid, dept_code, desg FROM supervisors"
        return self.db.fetch(query) or []

    def create_widgets(self):
        """Create all widgets in the supervisor constraints UI."""
        # Main content frame
        content_frame = ctk.CTkFrame(self, fg_color=FRAME_COLOR, corner_radius=10)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = ctk.CTkFrame(content_frame, fg_color=FRAME_COLOR)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Load and display logo
        try:
            logo = ctk.CTkImage(Image.open(os.path.join(BASE_DIR, "..","config", "logo.png")), size=(50, 50))
            ctk.CTkLabel(header_frame, image=logo, text="").pack(side="left", padx=(0, 10))
        except FileNotFoundError:
            print(os.path.join(BASE_DIR, "..","config", "logo.png"))
            print("Logo file not found.")

        ctk.CTkLabel(header_frame, text="Supervisor Constraints Management", font=FONT_H1, text_color=TEXT_COLOR).pack(side="left")

        # Supervisor selection frame
        selection_frame = ctk.CTkFrame(content_frame, fg_color=FRAME_COLOR)
        selection_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(selection_frame, text="Select Supervisor:", font=FONT_H3, text_color=TEXT_COLOR).pack(side="left", padx=(0, 10))
        self.supervisor_var = ctk.StringVar()
        self.supervisor_dropdown = ctk.CTkComboBox(selection_frame, variable=self.supervisor_var, values=[sup['name'] for sup in self.supervisors], font=FONT_H3, width=300, fg_color=BUTTON_COLOR, text_color=TEXT_COLOR, dropdown_fg_color=BUTTON_COLOR, dropdown_text_color=TEXT_COLOR, dropdown_hover_color=BUTTON_HOVER_COLOR)
        self.supervisor_dropdown.pack(side="left", padx=10)
        self.supervisor_dropdown.bind("<<ComboboxSelected>>", self.update_readonly_fields)

        # Supervisor details frame
        details_frame = ctk.CTkFrame(content_frame, fg_color=FRAME_COLOR)
        details_frame.pack(fill="x", padx=20, pady=10)

        # Supervisor fields (name, rfid, dept_code, desg)
        fields = [("Name:", 'name'), ("RFID:", 'rfid'), ("Dept Code:", 'dept_code'), ("Designation:", 'desg')]
        self.entries = {}
        for idx, (label, field) in enumerate(fields):
            field_frame = ctk.CTkFrame(details_frame, fg_color=FRAME_COLOR)
            field_frame.pack(fill="x", pady=5)
            ctk.CTkLabel(field_frame, text=label, font=FONT_H3, text_color=TEXT_COLOR, width=100).pack(side="left", padx=(0, 10))
            entry = ctk.CTkEntry(field_frame, font=FONT_H3, width=300, state="readonly", fg_color=BUTTON_COLOR, text_color=TEXT_COLOR)
            entry.pack(side="left")
            self.entries[field] = entry

        # Date selection frame
        date_frame = ctk.CTkFrame(content_frame, fg_color=FRAME_COLOR)
        date_frame.pack(fill="x", padx=20, pady=10)

        # Date entry fields for start and end date (editable)
        start_date_frame = ctk.CTkFrame(date_frame, fg_color=FRAME_COLOR)
        start_date_frame.pack(side="left", padx=(0, 20))
        ctk.CTkLabel(start_date_frame, text="Start Date:", font=FONT_H3, text_color=TEXT_COLOR).pack(side="left", padx=(0, 10))
        self.date_from = DateEntry(start_date_frame, font=FONT_H3, width=12, background=ACCENT_COLOR, foreground=TEXT_COLOR, borderwidth=2, date_pattern="yyyy-mm-dd")
        self.date_from.pack(side="left")

        end_date_frame = ctk.CTkFrame(date_frame, fg_color=FRAME_COLOR)
        end_date_frame.pack(side="left")
        ctk.CTkLabel(end_date_frame, text="End Date:", font=FONT_H3, text_color=TEXT_COLOR).pack(side="left", padx=(0, 10))
        self.date_to = DateEntry(end_date_frame, font=FONT_H3, width=12, background=ACCENT_COLOR, foreground=TEXT_COLOR, borderwidth=2, date_pattern="yyyy-mm-dd")
        self.date_to.pack(side="left")

        # Action buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color=FRAME_COLOR)
        button_frame.pack(pady=20)

        button_texts = [("Add", self.add), ("Update", self.update), ("Clear", self.clear)]
        for text, cmd in button_texts:
            button = ctk.CTkButton(button_frame, text=text, font=FONT_H3, width=120, command=cmd, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, corner_radius=8)
            button.pack(side="left", padx=10)

    def update_readonly_fields(self, _):
        print("update_readonly_fields debugging enabled")
        selected_name = self.supervisor_var.get()
        print("Selected supervisor:", selected_name)  # Debug: Check selected name
        
        supervisor = next((sup for sup in self.supervisors if sup['name'] == selected_name), None)
        if supervisor:
            print("Supervisor data:", supervisor)  # Debug: Check supervisor data
            for key, entry in self.entries.items():
                entry.configure(state="normal")
                entry.delete(0, ctk.END)
                entry.insert(0, supervisor[key])
                entry.configure(state="readonly")
        else:
            print("Supervisor not found!")  # Debugging message

    def add_or_update(self, query, success_msg):
        supervisor_name = self.supervisor_var.get()
        supervisor_id = next((sup['id'] for sup in self.supervisors if sup['name'] == supervisor_name), None)
        if not all([supervisor_id, self.date_from.get(), self.date_to.get()]):
            messagebox.showwarning("Required Fields", "Please complete all fields.")
            return
        try:
            self.db.exec(query, (self.date_from.get(), self.date_to.get(), supervisor_id))
            messagebox.showinfo(success_msg, f"Supervisor constraint {success_msg.lower()} successfully.")
            self.clear()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def add(self):
        self.add_or_update("UPDATE supervisors SET start_date=%s, end_date=%s WHERE id=%s", "Added")

    def update(self):
        self.add_or_update("UPDATE supervisors SET start_date=%s, end_date=%s WHERE id=%s", "Updated")

    def clear(self):
        """Clear all fields."""
        self.supervisor_dropdown.set('')
        for entry in self.entries.values():
            entry.configure(state="normal")
            entry.delete(0, ctk.END)
            entry.configure(state="readonly")
        self.date_from.set_date(None)
        self.date_to.set_date(None)

def display_module(root):
    """Display the Supervisor Constraints Management module."""
    for widget in root.winfo_children():
        widget.destroy()
    SupervisorConstraintsApp(root).pack(fill="both", expand=True)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Supervisor Constraints Management")
    root.geometry("800x600")
    display_module(root)
    root.mainloop()
