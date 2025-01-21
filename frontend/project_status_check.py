import os

def check_directory_status(directory):
    print(f"Checking directory: {directory}")
    if os.path.exists(directory):
        print(f"Found directory: {directory}")
    else:
        print(f"Missing directory: {directory}")
        os.makedirs(directory)
        print(f"Created missing directory: {directory}")

def check_file_status(file_path):
    print(f"Checking file: {file_path}")
    if os.path.exists(file_path):
        print(f"Found file: {file_path}")
    else:
        print(f"Missing file: {file_path}")
        # Here we could add code to create default files if required

def run_status_check():
    project_dir = os.path.expanduser("~/project_root/frontend")

    # Check Firebase configurations
    check_file_status(os.path.join(project_dir, "firebase.json"))
    check_file_status(os.path.join(project_dir, "storage.rules"))

    # Check directories for backend and AI model
    check_directory_status(os.path.join(project_dir, "backend/src"))
    check_directory_status(os.path.join(project_dir, "src/ai_model"))

    print("Status check complete!")

if __name__ == "__main__":
    run_status_check()
