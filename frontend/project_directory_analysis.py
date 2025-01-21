import os
import json

# Function to log the activities
def log_activity(message):
    with open("project_fix_report.txt", "a") as log_file:
        log_file.write(message + "\n")
        print(message)  # Also print to the console for real-time feedback

# Function to check if a file or directory exists
def check_file_or_dir(path):
    return os.path.exists(path)

# Function to create missing files or directories and log the action
def create_file_or_dir(path, file_type):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)  # Ensure the directory exists

    if file_type == "file":
        with open(path, 'w') as f:
            f.write("")  # Create an empty file
    elif file_type == "directory":
        os.makedirs(path, exist_ok=True)
    log_activity(f"Created missing {file_type}: {path}")

# Function to validate the project structure
def validate_project_structure(project_plan, project_root):
    for category, items in project_plan.items():
        for item in items:
            item_path = os.path.join(project_root, item)
            if not check_file_or_dir(item_path):
                log_activity(f"Missing {category}: {item} - Fixing...")
                if category == "files":
                    create_file_or_dir(item_path, "file")
                elif category == "directories":
                    create_file_or_dir(item_path, "directory")
            else:
                log_activity(f"Found {category}: {item} at {item_path}")

# Function to check and update firebase.json
def check_firebase_json(project_root):
    firebase_json_path = os.path.join(project_root, "firebase.json")
    if not check_file_or_dir(firebase_json_path):
        log_activity("firebase.json not found. Creating a default file...")
        create_file_or_dir(firebase_json_path, "file")
        # Add default structure to firebase.json
        with open(firebase_json_path, "w") as f:
            json.dump({
                "hosting": {
                    "public": "public",
                    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"]
                },
                "emulators": {
                    "hosting": {"host": "127.0.0.1", "port": 5000}
                }
            }, f, indent=4)
    else:
        log_activity("firebase.json found and is correct.")

# Main function to validate project against the plan
def main():
    # Example of project plan structure
    project_plan = {
        "files": ["firebase.json", "storage.rules"],
        "directories": ["public", "src", "backend/src"]
    }

    project_root = os.getcwd()  # Assuming you are in the project root directory

    log_activity("Starting project validation against the project plan...")

    # Validate the project structure
    validate_project_structure(project_plan, project_root)

    # Check and update firebase.json if needed
    check_firebase_json(project_root)

    log_activity("Project validation and fixes are complete.")

if __name__ == "__main__":
    main()
