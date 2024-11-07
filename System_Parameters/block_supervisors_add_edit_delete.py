import customtkinter as ctk
from tkinter import messagebox, ttk
import json
from config.db_connection import db


def display_module(master):
    """Display the Supervisor Management interface."""
    BlockSupervisorApp(master).grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


class BlockSupervisorApp(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master.configure(fg_color="#1E1E1E")
        self.data = self.load_data()
        self.fonts = self.data.get("fonts", {})  # Load fonts from the JSON
        self.create_widgets()

    def load_data(self):
        """Load department, role, and font data from JSON."""
        try:
            with open('config/data.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Error loading or parsing 'data.json'.")
            return {"departments": [], "roles": [], "fonts": {}}  # Return empty fonts if there's an error

    def create_widgets(self):
        """Create all the widgets for the supervisor management interface."""
        form_frame = ctk.CTkFrame(self, fg_color="#2E2E2E", corner_radius=15, border_width=2, border_color="#5D5D5D")
        form_frame.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")
        
        fields = ["Name of Block Supervisor", "Supervisor's RFID"]
        self.entries = {field: self.create_input_field(form_frame, field, idx) for idx, field in enumerate(fields)}
        
        self.create_dropdowns(form_frame)
        self.create_buttons()
        self.create_supervisor_table()
        self.load_supervisor_data()

    def create_input_field(self, parent, field, idx):
        """Helper method to create input fields."""
        font = self.get_font("h4")
        ctk.CTkLabel(parent, text=f"{field}:", font=font, text_color="#C7C7C7").grid(row=idx, column=0, sticky="e", pady=5)
        entry = ctk.CTkEntry(parent, font=font, width=200, corner_radius=8, fg_color="#3C3C3C")
        entry.grid(row=idx, column=1, pady=5, padx=10)
        return entry

    def create_dropdowns(self, parent):
        """Create department and designation dropdowns."""
        font = self.get_font("h4")
        self.department_var = ctk.StringVar()
        self.role_var = ctk.StringVar()

        ctk.CTkLabel(parent, text="Department:", font=font, text_color="#C7C7C7").grid(row=2, column=0, sticky="e", pady=5)
        department_dropdown = ctk.CTkComboBox(
            parent, variable=self.department_var, values=[dept["name"] for dept in self.data["departments"]],
            font=font, width=200, fg_color="#3C3C3C", border_width=0
        )
        department_dropdown.grid(row=2, column=1, pady=5, padx=10)

        ctk.CTkLabel(parent, text="Designation:", font=font, text_color="#C7C7C7").grid(row=3, column=0, sticky="e", pady=5)
        role_dropdown = ctk.CTkComboBox(
            parent, variable=self.role_var, values=self.data["roles"], font=font, width=200, fg_color="#3C3C3C", border_width=0
        )
        role_dropdown.grid(row=3, column=1, pady=5, padx=10)

    def create_buttons(self):
        """Create action buttons for managing supervisors."""
        button_frame = ctk.CTkFrame(self, fg_color="#2E2E2E", corner_radius=15)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        button_texts = ["Add", "Update", "Delete", "Clear"]
        button_commands = [self.add, self.update, self.delete, self.clear]

        for idx, (text, cmd) in enumerate(zip(button_texts, button_commands)):
            font = self.get_font("h4")
            button = ctk.CTkButton(button_frame, text=text, font=font, width=100, command=cmd, corner_radius=12, fg_color="#333333", hover_color="#4C4C4C", border_width=1, border_color="#444444")
            button.grid(row=0, column=idx, padx=10)

    def create_supervisor_table(self):
        """Create a table to display supervisor information."""
        columns = ("Name", "Department", "Designation", "RFID")
        
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=100)
        self.tree.grid(row=5, column=0, columnspan=2, pady=40, padx=20)

        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", width=200)

        style = ttk.Style()
        font = self.get_font("h4")
        style.configure("Treeview.Heading", font=font)  # Font for the headings
        style.configure("Treeview", font=font)  # Font for the rows

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=5, column=2, sticky='ns')

    def load_supervisor_data(self):
        """Load and display supervisor data from the database."""
        self.tree.delete(*self.tree.get_children())

        query = "SELECT name AS Name, dept_code AS Department, desg AS Designation, rfid AS RFID FROM supervisors"
        
        try:
            results = db.fetch(query)
            font = self.get_font("h4")
            style = ttk.Style()
            style.configure("Custom.Treeview", font=font, rowheight=35)  # Increased row height (30 pixels)
            self.tree.configure(style="Custom.Treeview")

            for row in results:
                dept_name = next((dept["name"] for dept in self.data["departments"] if dept["code"] == row["Department"]), row["Department"])
                self.tree.insert("", ctk.END, values=(row["Name"], dept_name, row["Designation"], row["RFID"]))
        except Exception as e:
            messagebox.showerror("Error", f"Error loading supervisor data: {e}")

    def add(self):
        """Add a new block supervisor entry."""
        form_data = {field: entry.get().strip() for field, entry in self.entries.items()}
        dept_code = next((dept["code"] for dept in self.data["departments"] if dept["name"] == self.department_var.get()), "")
        role = self.role_var.get().strip()

        if not all([form_data["Name of Block Supervisor"], form_data["Supervisor's RFID"], dept_code, role]):
            messagebox.showwarning("Incomplete Data", "Please fill in all fields before adding.")
            return

        query = "INSERT INTO supervisors (name, dept_code, desg, rfid) VALUES (%s, %s, %s, %s)"
        values = (form_data["Name of Block Supervisor"], dept_code, role, form_data["Supervisor's RFID"])

        try:
            db.exec(query, values)
            messagebox.showinfo("Success", "Block Supervisor added successfully.")
            self.load_supervisor_data()
            self.clear()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding supervisor: {e}")

    def update(self):
        """Update the selected supervisor."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a supervisor to update.")
            return

        selected_values = self.tree.item(selected_item[0], "values")
        form_data = {field: entry.get().strip() for field, entry in self.entries.items()}

        dept_code = next((dept["code"] for dept in self.data["departments"] if dept["name"] == self.department_var.get()), "")
        role = self.role_var.get().strip()

        if not all([form_data["Name of Block Supervisor"], form_data["Supervisor's RFID"], dept_code, role]):
            messagebox.showwarning("Incomplete Data", "Please fill in all fields before updating.")
            return

        query = "UPDATE supervisors SET name = %s, dept_code = %s, desg = %s, rfid = %s WHERE rfid = %s"
        values = (form_data["Name of Block Supervisor"], dept_code, role, form_data["Supervisor's RFID"], selected_values[3])

        try:
            db.exec(query, values)
            messagebox.showinfo("Success", "Block Supervisor updated successfully.")
            self.load_supervisor_data()
            self.clear()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating supervisor: {e}")

    def delete(self):
        """Delete the selected supervisor."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a supervisor to delete.")
            return

        selected_values = self.tree.item(selected_item[0], "values")
        query = "DELETE FROM supervisors WHERE rfid = %s"

        try:
            db.exec(query, (selected_values[3],))
            messagebox.showinfo("Success", "Block Supervisor deleted successfully.")
            self.load_supervisor_data()
            self.clear()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting supervisor: {e}")

    def clear(self):
        """Clear the input fields."""
        for entry in self.entries.values():
            entry.delete(0, ctk.END)
        self.department_var.set("")
        self.role_var.set("")

    def get_font(self, style):
        """Get the appropriate font based on the style."""
        font_data = self.fonts.get(style, ["Arial", 14, "normal"])
        return (font_data[0], font_data[1], font_data[2])


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Supervisor Management")
    display_module(root)
    root.mainloop()
