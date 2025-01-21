import os
import json
import shutil
import subprocess

def check_firebase_json():
    """Check if firebase.json is correctly configured."""
    print("Checking firebase.json configuration...")
    try:
        with open('firebase.json', 'r') as file:
            firebase_config = json.load(file)
        print("firebase.json loaded successfully.")
        
        # Check if storage rules are correctly specified in firebase.json
        if 'storage' not in firebase_config.get('emulators', {}):
            print("Error: Storage emulator configuration is missing in firebase.json.")
            return False
        
        if 'rules' not in firebase_config['emulators']['storage']:
            print("Error: Storage rules file is not specified in firebase.json.")
            return False
        
        print("firebase.json configuration seems correct.")
        return True
    except Exception as e:
        print(f"Error reading firebase.json: {e}")
        return False

def check_storage_rules():
    """Verify the presence of storage.rules and validate its content."""
    print("Checking storage.rules file...")
    if not os.path.exists('storage.rules'):
        print("Error: storage.rules file is missing.")
        return False
    
    # Basic validation of the storage.rules file content
    with open('storage.rules', 'r') as file:
        rules_content = file.read()
    
    if 'firebase.storage' not in rules_content:
        print("Error: Invalid content in storage.rules file.")
        return False

    print("storage.rules file is valid.")
    return True

def check_for_existing_emulators():
    """Check if the emulators are already running on the specified ports."""
    print("Checking if any emulators are running on required ports...")
    ports_to_check = [5000, 9099, 9199, 8080, 4000]  # Add more ports as needed
    for port in ports_to_check:
        result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
        if result.stdout:
            print(f"Port {port} is already in use. You may need to stop the service running on it.")
            return False
    print("No conflicting processes found on required ports.")
    return True

def fix_firebase_json():
    """Attempt to fix common errors in firebase.json."""
    print("Attempting to fix firebase.json...")
    
    # Check if the rules key is set correctly
    with open('firebase.json', 'r') as file:
        firebase_config = json.load(file)
    
    if 'emulators' in firebase_config:
        if 'storage' not in firebase_config['emulators']:
            print("Adding missing storage emulator configuration...")
            firebase_config['emulators']['storage'] = {
                "host": "127.0.0.1",
                "port": 9199,
                "rules": "storage.rules"
            }

        # Write the changes back to firebase.json
        with open('firebase.json', 'w') as file:
            json.dump(firebase_config, file, indent=2)
        print("firebase.json has been updated.")

def start_emulators():
    """Attempt to start Firebase emulators."""
    print("Starting Firebase emulators...")
    try:
        result = subprocess.run(['firebase', 'emulators:start', '--debug'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Emulators started successfully.")
        else:
            print(f"Error starting emulators: {result.stderr}")
    except Exception as e:
        print(f"Error starting emulators: {e}")

def main():
    """Main function to execute troubleshooting and fix errors."""
    print("Starting Firebase Emulator Troubleshooter...")

    # Step 1: Check firebase.json configuration
    if not check_firebase_json():
        print("Please fix the issues in firebase.json manually.")
        return
    
    # Step 2: Check storage.rules file
    if not check_storage_rules():
        print("Please fix the issues in storage.rules manually.")
        return
    
    # Step 3: Check for existing emulator conflicts
    if not check_for_existing_emulators():
        print("Please close the applications running on the conflicting ports and try again.")
        return
    
    # Step 4: Fix common errors in firebase.json if any
    fix_firebase_json()
    
    # Step 5: Start emulators
    start_emulators()

if __name__ == "__main__":
    main()
