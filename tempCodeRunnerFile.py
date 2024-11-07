import customtkinter as ctk
import json
import os
import webbrowser

def load_json(file_path):
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
    """Display HomeScreen."""
    for widget in root.winfo_children(): widget.destroy()
    landing_page = LandingPage()
    landing_page.grid(row=0, column=0, sticky="nsew")

class LandingPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Exam Seating Arrangement System")
        self.geometry("1000x600")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.data = load_json('config/data.json')
        self.institute_data = self.data.get("institute", {})
        self.dev_info = self.data.get("dev", {})

        self.create_widgets()

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Institute Information
        self.create_institute_frame(main_frame)

        # Content Frame
        content_frame = ctk.CTkTabview(main_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", pady=(20, 0))
        
        # Software Info Tab
        software_tab = content_frame.add("Software Info")
        self.create_software_info(software_tab)

        # Features Tab
        features_tab = content_frame.add("Features")
        self.create_features(features_tab)

        # Contact Tab
        contact_tab = content_frame.add("Contact")
        self.create_contact_info(contact_tab)

    def create_institute_frame(self, parent):
        institute_frame = ctk.CTkFrame(parent, fg_color="#1e3a1e")
        institute_frame.grid(row=0, column=0, sticky="ew")
        institute_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(institute_frame, text=self.institute_data.get("INS_NAME", "Institute Name Not Found"), 
                     font=ctk.CTkFont(size=32, weight="bold")).grid(row=0, column=0, pady=5)
        ctk.CTkLabel(institute_frame, text=self.institute_data.get("INS_ADDRESS", "Address Not Found")).grid(row=1, column=0)
        ctk.CTkLabel(institute_frame, text=f"Exam Center: {self.institute_data.get('EXAM_CENTER', 'Not Specified')}").grid(row=2, column=0)

    def create_software_info(self, parent):
        ctk.CTkLabel(parent, text="Exam Seating Arrangement System", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)
        ctk.CTkLabel(parent, text="Version: 1.0.0", text_color="gray").pack()
        ctk.CTkLabel(parent, text="This software helps in managing the seating arrangement for exams, keeping track of blocks, supervisors, and students.", 
                     wraplength=500, justify="center").pack(pady=20)

    def create_features(self, parent):
        features = {
            "Seating Arrangement Management": "Manage seating assignments for students across multiple blocks.",
            "Supervisor and Block Management": "Assign supervisors to blocks and keep track of their duties.",
            "Automatic Generation of Seating Plans": "Generate seating plans automatically based on various parameters.",
            "Real-time Data Updates": "Keep track of real-time changes and updates during the exam period.",
            "Easy-to-use Interface": "The system has a user-friendly interface for easy navigation."
        }

        for feature, description in features.items():
            feature_frame = ctk.CTkFrame(parent)
            feature_frame.pack(pady=10, padx=20, fill="x")
            
            feature_label = ctk.CTkButton(feature_frame, text=feature, font=ctk.CTkFont(size=16, weight="bold"),
                                          command=lambda f=feature, d=description: self.show_feature_details(f, d))
            feature_label.pack(pady=5, fill="x")
            
            description_label = ctk.CTkLabel(feature_frame, text=description, wraplength=400, justify="left", font=ctk.CTkFont(size=14))
            description_label.pack(pady=(5, 10), padx=10)

    def create_contact_info(self, parent):
        contact_details = [
            ("Phone", self.dev_info.get('phone')),
            ("Email", self.dev_info.get('email')),
            ("Website", self.dev_info.get('website')),
            ("Address", self.dev_info.get('address'))
        ]
        for label, value in contact_details:
            frame = ctk.CTkFrame(parent)
            frame.pack(pady=5, padx=20, fill="x")
            ctk.CTkLabel(frame, text=f"{label}:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))
            ctk.CTkLabel(frame, text=value).pack(side="left")

        ctk.CTkButton(parent, text="Contact Us", command=self.open_website, 
                      font=ctk.CTkFont(size=16, weight="bold"), height=40).pack(pady=20)

    def show_feature_details(self, feature, description):
        # Display feature details within the tab, without using a dialog box.
        feature_details_window = ctk.CTkToplevel(self)
        feature_details_window.title(f"{feature} Details")
        feature_details_window.geometry("400x300")
        
        ctk.CTkLabel(feature_details_window, text=feature, font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        ctk.CTkLabel(feature_details_window, text=description, wraplength=350, justify="left", font=ctk.CTkFont(size=14)).pack(padx=20)

    def open_website(self):
        webbrowser.open_new(self.dev_info.get('website', 'https://example.com'))

if __name__ == "__main__":
    app = LandingPage()
    app.mainloop()
