from distutils.core import setup
import py2exe
import os
import glob

# Collect all data files you need (non-Python files)
data_files = [
    ("", ["modules.json", ".env", "institute_info.env"]),  # Root-level data files
    ("Absent_Copy_Case_Nos", glob.glob("Absent_Copy_Case_Nos/*.py")),  # Files in Absent_Copy_Case_Nos
    ("config", glob.glob("config/*.py")),  # Files in config
    ("Exam_Block_Details", glob.glob("Exam_Block_Details/*.py")),  # Files in Exam_Block_Details
    ("Exam_Examinee_Details", glob.glob("Exam_Examinee_Details/*.py")),  # Files in Exam_Examinee_Details
    ("Exit", glob.glob("Exit/*.py")),  # Files in Exit
    ("Reports", glob.glob("Reports/*.py")),  # Files in Reports
    ("System_Parameters", glob.glob("System_Parameters/*.py")),  # Files in System_Parameters
    ("System_Tools", glob.glob("System_Tools/*.py")),  # Files in System_Tools
]

# Define the setup function
setup(
    windows=["app.py"],  # Entry-point script
    options={
        "py2exe": {
            "packages": ["customtkinter", "tkinter"],  # Include necessary packages
            "bundle_files": 1,  # Bundle everything into a single exe if needed
            "compressed": True,
        }
    },
    data_files=data_files,  # Add additional files
)
