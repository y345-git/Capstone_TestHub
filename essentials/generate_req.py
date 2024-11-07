import os
import ast
import pkg_resources
import sys

def get_imports_from_file(file_path):
    """Parse a Python file and return a set of imported modules."""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split('.')[0])  # Only take the module name, not submodules
                elif isinstance(node, ast.ImportFrom):
                    imports.add(node.module.split('.')[0])  # For 'from module import ...'
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    return imports

def find_python_files(directory):
    """Recursively find all Python files in the given directory."""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def get_installed_modules():
    """Return a set of installed modules in the current environment."""
    return {pkg.key for pkg in pkg_resources.working_set}

def create_requirements_file(directory, output_file="requirements.txt"):
    """Create a requirements.txt file by scanning all Python files in a directory."""
    all_imports = set()
    
    # Find all Python files in the directory
    python_files = find_python_files(directory)
    
    for file in python_files:
        imports = get_imports_from_file(file)
        all_imports.update(imports)
    
    # Get installed modules
    installed_modules = get_installed_modules()
    
    # Filter out non-installed modules (local/internal imports may be excluded)
    required_modules = sorted(all_imports.intersection(installed_modules))
    
    # Define the additional required modules
    additional_modules = ["mysql-connector-python", "python-dotenv"]
    
    # Merge the required and additional modules
    required_modules.extend(additional_modules)
    
    # Write to requirements.txt with two new lines between each entry
    with open(output_file, 'w', encoding='utf-8') as req_file:
        for module in required_modules:
            req_file.write(f"{module}\n\n")
    
    print(f"requirements.txt has been created with {len(required_modules)} modules.")

if __name__ == "__main__":
    directory = input("Enter the path to the folder: ")
    create_requirements_file(directory)
