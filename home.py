import customtkinter as ctk
import json
import os
import webbrowser

def load_json(file_path):
    """Load JSON data from the specified file path."""
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return {}
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{file_path}'.")
        return {}

def display_module(root):
    """Display the main application interface."""
    for widget in root.winfo_children():
        widget.destroy()

    class LandingPage(ctk.CTkFrame):
        def __init__(self, master):
            super().__init__(master)
            self.pack(fill="both", expand=True)

            # Load configuration data
            self.data = load_json('config/data.json')
            self.institute_data = self.data.get("institute", {})
            self.dev_info = self.data.get("dev", {})

            self.create_widgets()

        def create_widgets(self):
            """Create the main widgets for the application."""
            # Institute Information
            self.create_institute_frame()

            # Tab view for different sections
            self.content_frame = ctk.CTkTabview(self)
            self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Software Info Tab
            software_tab = self.content_frame.add("Software Info")
            self.create_software_info(software_tab)

            # Features Tab
            features_tab = self.content_frame.add("Features")
            self.create_features(features_tab)

            # Contact Tab
            contact_tab = self.content_frame.add("Contact")
            self.create_contact_info(contact_tab)

        def create_institute_frame(self):
            """Create a frame displaying institute information."""
            institute_frame = ctk.CTkFrame(self, fg_color="#2e2e2e")
            institute_frame.pack(fill="x", padx=20, pady=(20, 0))
            
            ctk.CTkLabel(institute_frame, text=self.institute_data.get("INS_NAME", "Institute Name Not Found"), 
                         font=ctk.CTkFont(size=32, weight="bold"), text_color="#F0E68C").pack(pady=5)
            ctk.CTkLabel(institute_frame, text=self.institute_data.get("INS_ADDRESS", "Address Not Found"), text_color="#FFFFFF").pack()
            ctk.CTkLabel(institute_frame, text=f"Exam Center: {self.institute_data.get('EXAM_CENTER', 'Not Specified')}", text_color="#FFFFFF").pack()

        def create_software_info(self, parent):
            """Create the software information section."""
            ctk.CTkLabel(parent, text="Exam Seating Arrangement System", font=ctk.CTkFont(size=24, weight="bold"), text_color="#FFDD44").pack(pady=10)
            ctk.CTkLabel(parent, text="Version: 1.0.0", text_color="gray").pack()
            ctk.CTkLabel(parent, text="This software helps in managing the seating arrangement for exams, keeping track of blocks, supervisors, and students.", 
                         wraplength=500, justify="center", text_color="#FFFFFF").pack(pady=20)

        def create_features(self, parent):
            """Create the features section."""
            features = {
                "Seating Arrangement Management": "Manage seating assignments for students across multiple blocks.",
                "Supervisor and Block Management": "Assign supervisors to blocks and keep track of their duties.",
                "Automatic Generation of Seating Plans": "Generate seating plans automatically based on various parameters.",
                "Real-time Data Updates": "Keep track of real-time changes and updates during the exam period.",
                "Easy-to-use Interface": "The system has a user-friendly interface for easy navigation."
            }
            main_frame = ctk.CTkScrollableFrame(parent)
            main_frame.pack(pady=10, padx=20, fill="x")

            for feature, description in features.items():
                feature_frame = ctk.CTkFrame(main_frame, fg_color="#3e3e3e")
                feature_frame.pack(pady=10, padx=20, fill="x")

                feature_label = ctk.CTkLabel(feature_frame, text=feature, font=ctk.CTkFont(size=16, weight="bold"), text_color="#FFDD44")
                feature_label.pack(pady=5, fill="x")

                description_label = ctk.CTkLabel(feature_frame, text=description, wraplength=400, justify="left", font=ctk.CTkFont(size=14), text_color="#FFFFFF")
                description_label.pack(pady=(5, 10), padx=10)

        def create_contact_info(self, parent):
            """Create the contact information section."""
            contact_details = [
                ("Phone", self.dev_info.get('phone', 'Not Available')),
                ("Email", self.dev_info.get('email', 'Not Available')),
                ("Website", self.dev_info.get('website', 'Not Available')),
                ("Address", self.dev_info.get('address', 'Not Available'))
            ]
            for label, value in contact_details:
                frame = ctk.CTkFrame(parent, fg_color="#2e2e2e")
                frame.pack(pady=5, padx=20, fill="x")
                ctk.CTkLabel(frame, text=f"{label}:", font=ctk.CTkFont(weight="bold"), text_color="#FFDD44").pack(side="left", padx=(0, 10))
                ctk.CTkLabel(frame, text=value, text_color="#FFFFFF").pack(side="left")

            ctk.CTkButton(parent, text="Contact Us", command=self.open_website, 
                          font=ctk.CTkFont(size=16, weight="bold"), height=40, fg_color="#FFDD44", text_color="#2e2e2e").pack(pady=20)

        def open_website(self):
            """Open the website in a web browser."""
            webbrowser.open_new(self.dev_info.get('website', 'https://example.com'))

    # Create and display the LandingPage
    LandingPage(root)

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Exam Seating Arrangement System")
    root.geometry("1000x600")
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    display_module(root)
    root.mainloop()