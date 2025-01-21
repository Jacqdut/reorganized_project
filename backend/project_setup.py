import os
import shutil
import subprocess
import json

# Paths and settings
BASE_DIR = "/home/jacqdut/combined_project"
BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
STATIC_DIR = os.path.join(BACKEND_DIR, "static")
FIREBASE_CONFIG = os.path.join(BACKEND_DIR, "firebase_service_account.json")


# Step 1: Clean and Restructure the Directories
def restructure_directories():
    print("Restructuring directories...")
    required_dirs = [BACKEND_DIR, FRONTEND_DIR, STATIC_DIR]

    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Move backend files
    for file in ["server.py", "requirements.txt"]:
        src = os.path.join(BASE_DIR, file)
        dest = os.path.join(BACKEND_DIR, file)
        if os.path.exists(src):
            shutil.move(src, dest)

    # Ensure Firebase configuration is in place
    if not os.path.exists(FIREBASE_CONFIG):
        print(f"ERROR: Firebase config not found at {FIREBASE_CONFIG}")
        return False

    print("Directories restructured successfully.")
    return True


# Step 2: Validate Firebase Configuration
def validate_firebase_config():
    print("Validating Firebase configuration...")
    try:
        with open(FIREBASE_CONFIG, "r") as f:
            config = json.load(f)
        required_keys = ["type", "project_id", "private_key", "client_email"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing key: {key}")
        print("Firebase configuration is valid.")
        return True
    except Exception as e:
        print(f"Firebase configuration error: {e}")
        return False


# Step 3: Install Backend Dependencies
def install_backend_dependencies():
    print("Installing backend dependencies...")
    result = subprocess.run(
        ["pip", "install", "-r", os.path.join(BACKEND_DIR, "requirements.txt")],
        capture_output=True,
    )
    if result.returncode != 0:
        print(f"Error installing dependencies: {result.stderr.decode()}")
        return False
    print("Backend dependencies installed successfully.")
    return True


# Step 4: Frontend Setup
def setup_frontend():
    print("Setting up frontend...")
    if not os.path.exists(os.path.join(FRONTEND_DIR, "package.json")):
        print("Frontend project not initialized. Running `npx create-react-app`...")
        result = subprocess.run(
            ["npx", "create-react-app", FRONTEND_DIR], capture_output=True
        )
        if result.returncode != 0:
            print(f"Error creating React app: {result.stderr.decode()}")
            return False
    print("Frontend setup complete.")
    return True


# Step 5: Test Backend
def test_backend():
    print("Testing backend...")
    try:
        result = subprocess.run(
            ["python3", os.path.join(BACKEND_DIR, "server.py")], capture_output=True
        )
        if result.returncode != 0:
            print(f"Backend test failed: {result.stderr.decode()}")
            return False
    except Exception as e:
        print(f"Error testing backend: {e}")
        return False
    print("Backend test passed successfully.")
    return True


# Step 6: Cleanup Duplicate Files
def cleanup_duplicates():
    print("Cleaning up duplicate files...")
    seen_files = set()
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            if file in seen_files:
                os.remove(file_path)
                print(f"Removed duplicate: {file_path}")
            else:
                seen_files.add(file)
    print("Duplicate cleanup complete.")


# Step 7: Run Full Project
def run_project():
    print("Running full project...")
    backend_process = subprocess.Popen(
        ["python3", os.path.join(BACKEND_DIR, "server.py")]
    )
    print("Backend running at: http://localhost:5000")
    print("You can now start the frontend manually if required.")
    return True


# Main Workflow
def main():
    if not restructure_directories():
        print("Failed to restructure directories.")
        return
    if not validate_firebase_config():
        print("Invalid Firebase configuration.")
        return
    if not install_backend_dependencies():
        print("Failed to install backend dependencies.")
        return
    if not setup_frontend():
        print("Failed to set up frontend.")
        return
    if not test_backend():
        print("Backend test failed.")
        return
    cleanup_duplicates()
    run_project()
    print("Project setup complete. Ready to test!")


if __name__ == "__main__":
    main()
