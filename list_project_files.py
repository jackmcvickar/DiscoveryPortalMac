import os
import argparse

parser = argparse.ArgumentParser(description='List project files with optional debug output')
parser.add_argument('--debug', action='store_true', help='Enable debug output')
args = parser.parse_args()

project_root = '.'  # Change this to your project root folder if needed

# Folders and files to exclude
exclude_dirs = {'.git', 'venv', 'node_modules', '__pycache__', 'tests', 'test', '.pytest_cache'}
exclude_files = {'test.py', 'tests.py'}  # Add any specific test files or patterns here
exclude_extensions = {'.pdf'}  # Exclude PDF files from test data

def debug_print(msg):
    if args.debug:
        print(f"DEBUG: {msg}")

for root, dirs, files in os.walk(project_root):
    debug_print(f"Processing directory: {root}")
    debug_print(f"Initial dirs: {dirs}")
    debug_print(f"Initial files: {files}")

    # Exclude the entire 'data' folder except for the single file 'dda.db'
    if os.path.basename(root).lower() == 'data':
        # Remove all dirs inside 'data' to prevent descending
        dirs[:] = []
        # Filter files to only include 'dda.db'
        files[:] = [f for f in files if f.lower() == 'dda.db']
        debug_print(f"Filtered files in 'data': {files}")

    # Modify dirs in-place to skip excluded directories
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    debug_print(f"Filtered dirs: {dirs}")

    level = root.replace(project_root, '').count(os.sep)
    indent = ' ' * 4 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 4 * (level + 1)
    for f in files:
        if (f not in exclude_files and
            not any(f.startswith(prefix) for prefix in ('test', 'Test')) and
            not any(f.endswith(ext) for ext in exclude_extensions)):
            print(f'{subindent}{f}')

# End of script