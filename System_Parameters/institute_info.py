import customtkinter as ctk
import json
from tkcalendar import DateEntry
from datetime import datetime

# Load font data from the JSON configuration file
def load_fonts():
    try:
        with open('config/data.json', 'r') as f:
            data = json.load(f)
            return data.get("fonts", {})
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error loading font data.")
        return {}

# Define font sizes based on loaded JSON
fonts = load_fonts()
HEADING_FONT = tuple(fonts.get("h2", ["Lexend", 24, "bold"]))
NORMAL_FONT = tuple(fonts.get("h4", ["Lexend", 14, "normal"]))
BUTTON_FONT = tuple(fonts.get("h4", ["Lexend", 14, "normal"]))

# Color scheme
BACKGROUND_COLOR = "#1a1a1a"
FRAME_COLOR = "#2a2a2a"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#3a7ebf"

# Update data.json with new institute and exam details
def update_data_json(institute_data, exam_data):
    try:
        with open('config/data.json', 'r') as f:
            data = json.load(f)
        
        # Update institute and exam details
        data['institute'] = institute_data
        data['exam_details'] = exam_data
        
        with open('config/data.json', 'w') as f:
            json.dump(data, f, indent=4)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error updating data.json: {e}")

# Display the main UI for managing institute and exam info
def display_module(root):
    # Clear existing widgets
    for widget in root.winfo_children(): widget.destroy()

    # Main frame
    main_frame = ctk.CTkFrame(root, fg_color=BACKGROUND_COLOR)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Header
    header_frame = ctk.CTkFrame(main_frame, fg_color=FRAME_COLOR, corner_radius=10)
    header_frame.pack(fill="x", pady=(0, 20))
    ctk.CTkLabel(header_frame, text="Institute Information", font=HEADING_FONT, text_color=TEXT_COLOR).pack(side="left", padx=20, pady=20)

    # Content frame
    content_frame = ctk.CTkFrame(main_frame, fg_color=FRAME_COLOR, corner_radius=10)
    content_frame.pack(fill="both", expand=True, pady=10)

    # Create fields dynamically
    fields = [
        ("Inst. Code of Exam Center", "INS_CODE"), 
        ("Name Of Examination Center", "INS_NAME"), 
        ("Examination Center Address", "INS_ADDRESS")
    ]
    for field, key in fields:
        create_readonly_field(content_frame, field, get_json_value(key))

    # Exam period selection (Summer/Winter)
    exam_period = ctk.StringVar(value=get_json_value("EXAM_PERIOD", "0"))
    create_exam_period_section(content_frame, exam_period)

    # Date fields for exam start and end dates
    start_entry, end_entry = create_date_fields(content_frame)

    # Save button
    ctk.CTkButton(content_frame, text="Save Changes", font=BUTTON_FONT, fg_color=ACCENT_COLOR, hover_color="#2a5d8f",
                  command=lambda: save_changes(content_frame, exam_period, start_entry, end_entry)).pack(pady=30)

# Create a readonly field with label and value from JSON
def create_readonly_field(parent, field, value):
    frame = ctk.CTkFrame(parent, fg_color=FRAME_COLOR)
    frame.pack(fill="x", pady=10, padx=20)
    ctk.CTkLabel(frame, text=f"{field}:", width=30, anchor="w", font=NORMAL_FONT, text_color=TEXT_COLOR).pack(side="left", padx=10)
    entry = ctk.CTkEntry(frame, state="readonly", textvariable=ctk.StringVar(value=value), font=NORMAL_FONT, fg_color=BACKGROUND_COLOR, text_color=TEXT_COLOR)
    entry.pack(side="left", fill="x", expand=True, padx=10)

# Create the exam period selection section (Summer/Winter)
def create_exam_period_section(parent, exam_period):
    period_frame = ctk.CTkFrame(parent, fg_color=FRAME_COLOR)
    period_frame.pack(fill="x", pady=15, padx=20)
    ctk.CTkLabel(period_frame, text="Theory Examination Details:", width=25, anchor="w", font=NORMAL_FONT, text_color=TEXT_COLOR).pack(side="left", padx=10)
    for text, value in [("Summer", "0"), ("Winter", "1")]:
        ctk.CTkRadioButton(period_frame, text=text, variable=exam_period, value=value, font=NORMAL_FONT, fg_color=ACCENT_COLOR, text_color=TEXT_COLOR).pack(side="left", padx=15)

# Create date entry fields for exam start and end dates
def create_date_fields(parent):
    start_date = get_json_date("EXAM_START_DATE")
    end_date = get_json_date("EXAM_END_DATE")
    
    return create_date_entry(parent, "Exam Start Date:", start_date), create_date_entry(parent, "Exam End Date:", end_date)

# Create a date entry field with label
def create_date_entry(parent, label, default_date):
    date_frame = ctk.CTkFrame(parent, fg_color=FRAME_COLOR)
    date_frame.pack(fill="x", pady=10, padx=20)
    ctk.CTkLabel(date_frame, text=label, width=25, anchor="w", font=NORMAL_FONT, text_color=TEXT_COLOR).pack(side="left", padx=10)
    entry = DateEntry(date_frame, font=NORMAL_FONT, year=default_date.year, month=default_date.month, day=default_date.day, 
                      date_pattern="yyyy-mm-dd", background=ACCENT_COLOR, foreground=TEXT_COLOR, borderwidth=2)
    entry.pack(side="left", fill="x", expand=True, padx=10)
    return entry

# Retrieve a value from the JSON configuration file
def get_json_value(key, section="institute", default_value="N/A"):
    try:
        with open('config/data.json', 'r') as f:
            data = json.load(f)
        return data.get(section, {}).get(key, default_value)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error retrieving {key} from JSON.")
        return default_value

# Retrieve a date from the JSON configuration file
def get_json_date(var_name, section="exam_details", default_date="2000-01-01"):
    date_str = get_json_value(var_name, section, default_date)
    return datetime.strptime(date_str, "%Y-%m-%d").date()

# Save changes to the institute and exam details in the JSON file
def save_changes(parent, exam_period, start_entry, end_entry):
    # Prepare new institute and exam data for JSON
    institute_data = {
        "INS_CODE": "1740",
        "INS_NAME": "Rajarambapu Institute of Technology",
        "INS_ADDRESS": "RAJARAMNAGAR",
        "EXAM_CENTER": "Main Campus",
        "DISTRIBUTION_CENTER": "Central Library"
    }
    
    exam_data = {
        "EXAM_PERIOD": exam_period.get(),
        "EXAM_START_DATE": start_entry.get_date().strftime("%Y-%m-%d"),
        "EXAM_END_DATE": end_entry.get_date().strftime("%Y-%m-%d")
    }

    # Update data.json with new institute and exam details
    update_data_json(institute_data, exam_data)

    # Show success message
    success_label = ctk.CTkLabel(parent, text="Changes saved successfully!", font=NORMAL_FONT, text_color="#4CAF50")
    success_label.pack(pady=15)
    parent.after(3000, success_label.destroy)  # Remove the message after 3 seconds

if __name__ == "__main__":
    # Set the appearance mode to dark and use the blue color theme
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Institute Information")
    root.geometry("600x700")  # Set a fixed size for the window
    root.configure(fg_color=BACKGROUND_COLOR)

    # Display the main module
    display_module(root)

    # Start the GUI main loop
    root.mainloop()
