import tkinter as tk
import customtkinter as ctk
import json
import importlib.util
import os

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Exam Seating Arrangement System")
        self.state("zoomed")

        # Load fonts and config from JSON
        self.config_data = self.load_config_data()
        self.HEADING_FONT = tuple(self.config_data['fonts']['h1'])
        self.NORMAL_FONT = tuple(self.config_data['fonts']['h4'])

        # Load modules and create UI
        self.modules = self.load_modules_data()
        self.create_header()
        self.create_footer()
        self.create_content_frame()
        self.create_menu_bar()
        self.show_home_screen()

    def load_config_data(self):
        """Load configuration from JSON file."""
        try:
            with open('config/data.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.display_error(f"Error loading config: {e}")
            return {}


    def load_modules_data(self):
        """Load modules from JSON file."""
        file_path = 'modules.json'
        try:
            with open(file_path, 'r') as file:
                return json.load(file).get('modules', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.display_error(f"Error loading 'modules.json': {e}")
            return []

    def create_header(self):
        ctk.CTkLabel(
            self, text="Exam Seating Arrangement System", font=self.HEADING_FONT,
            text_color="black", fg_color="#FFD700").pack(fill="x", pady=10)

    def create_footer(self):
        ctk.CTkLabel(
            self, text="© 2024 Seating Arrangement System. All rights reserved.",
            font=self.NORMAL_FONT, text_color="black", fg_color="#FFD700").pack(fill="x", side="bottom", pady=5)

    def create_content_frame(self):
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(padx=70, pady=70, fill="both", expand=True)

    def create_menu_bar(self):
        """Create dynamic menu bar from modules data."""
        menu_bar = tk.Menu(self)
        for module in self.modules:
            module_menu = tk.Menu(menu_bar, tearoff=0)
            self.add_submodules_to_menu(module, module_menu)
            menu_bar.add_cascade(label=module['module_name'], menu=module_menu)
        menu_bar.add_command(label="Exit", command=self.quit)
        self.config(menu=menu_bar)

    def add_submodules_to_menu(self, module, module_menu):
        """Add submodules to menu."""
        for submodule in module.get('submodules', []):
            if 'submodules' in submodule:
                sub_menu = tk.Menu(module_menu, tearoff=0)
                for item in submodule.get('submodules', []):
                    sub_menu.add_command(label=item['name'], command=lambda s=item: self.show_frame(s))
                module_menu.add_cascade(label=submodule['name'], menu=sub_menu)
            else:
                module_menu.add_command(label=submodule['name'], command=lambda s=submodule: self.show_frame(s))

    def show_home_screen(self):
        """Show home screen."""
        self.show_frame({"name": "Home", "file": "home.py"})

    def show_frame(self, submodule):
        """Load content from selected submodule."""
        self.clear_content_frame()
        self.title(f"{submodule.get('name', 'Main Menu')} | Seating Arrangement System")
        self.execute_file(submodule.get("file"))

    def clear_content_frame(self):
        """Clear content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def execute_file(self, file_path):
        """Execute file and load display function if available."""
        file_path = os.path.abspath(file_path)  # Using absolute path
        if os.path.exists(file_path):
            try:
                spec = importlib.util.spec_from_file_location("module.name", file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, 'display_module'):
                    module.display_module(self.content_frame)
                else:
                    self.display_message("No display function found in module.")
            except Exception as e:
                self.display_error(f"Error executing '{file_path}': {str(e)}")
        else:
            self.display_error(f"Error: '{file_path}' not found.")

    def display_message(self, message):
        """Display message in content frame."""
        ctk.CTkLabel(self.content_frame, text=message, font=self.NORMAL_FONT, text_color="black").pack(pady=20)

    def display_error(self, error_message):
        """Display error message."""
        ctk.CTkLabel(self.content_frame, text=error_message, font=self.NORMAL_FONT, text_color="red").pack(pady=10)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
