import os
import shutil
import subprocess
import json

BASE_DIR = "/home/jacqdut/combined_project"
REQUIRED_DIRS = {
    "backend": ["static", "tests"],
    "frontend": ["src", "build"],
    "database": ["mongodb"],
    "scripts": [],
}

REQUIRED_FILES = {
    "backend": [
        "server.py",
        "requirements.txt",
        "firebase_service_account.json",
        "static/swagger.json",
    ],
    "frontend": ["package.json", ".env"],
}


def ensure_directories():
    for folder, subfolders in REQUIRED_DIRS.items():
        folder_path = os.path.join(BASE_DIR, folder)
        os.makedirs(folder_path, exist_ok=True)
        for subfolder in subfolders:
            os.makedirs(os.path.join(folder_path, subfolder), exist_ok=True)
    print("[INFO] Directories structured successfully.")


def move_files():
    for folder, files in REQUIRED_FILES.items():
        for file in files:
            for root, _, filenames in os.walk(BASE_DIR):
                if file in filenames:
                    src = os.path.join(root, file)
                    dest = os.path.join(BASE_DIR, folder, file)
                    if src != dest:
                        shutil.move(src, dest)
    print("[INFO] Files moved to their correct locations.")


def clean_duplicates():
    unique_files = set()
    for root, _, filenames in os.walk(BASE_DIR):
        for filename in filenames:
            if filename in unique_files:
                os.remove(os.path.join(root, filename))
            else:
                unique_files.add(filename)
    print("[INFO] Duplicate files removed.")


def validate_firebase_config():
    fb_path = os.path.join(BASE_DIR, "backend/firebase_service_account.json")
    try:
        with open(fb_path, "r") as f:
            config = json.load(f)
            required_keys = ["type", "project_id", "private_key", "client_email"]
            if all(key in config for key in required_keys):
                print("[INFO] Firebase configuration is valid.")
            else:
                print("[ERROR] Firebase configuration is missing required keys.")
    except Exception as e:
        print(f"[ERROR] Firebase configuration error: {e}")


def test_scripts():
    backend_dir = os.path.join(BASE_DIR, "backend")
    try:
        result = subprocess.run(
            ["python3", os.path.join(backend_dir, "server.py")],
            capture_output=True,
            text=True,
        )
        print(f"[INFO] Server test output:\n{result.stdout}")
        if result.stderr:
            print(f"[ERROR] Server test errors:\n{result.stderr}")
    except Exception as e:
        print(f"[ERROR] Failed to test server script: {e}")


def main():
    print("[INFO] Starting project restructuring...")
    ensure_directories()
    move_files()
    clean_duplicates()
    validate_firebase_config()
    test_scripts()
    print("[INFO] Project restructuring complete.")


if __name__ == "__main__":
    main()
