import os
import shutil

def list_scripts(directory):
    scripts = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                scripts.append(os.path.join(root, file))
    return scripts

def categorize_scripts(scripts):
    categories = {
        'frontend': [],
        'backend': [],
        'models/training': [],
        'models/inspection': [],
        'reports': [],
        'scripts': [],
        'tests': []
    }

    for script in scripts:
        if 'frontend' in script or 'front' in script:
            categories['frontend'].append(script)
        elif 'backend' in script or 'back' in script:
            categories['backend'].append(script)
        elif 'training' in script or 'train' in script:
            categories['models/training'].append(script)
        elif 'inspection' in script or 'inspect' in script:
            categories['models/inspection'].append(script)
        elif 'report' in script:
            categories['reports'].append(script)
        elif 'test' in script:
            categories['tests'].append(script)
        else:
            categories['scripts'].append(script)
    
    return categories

def move_scripts(categorized_scripts, base_directory):
    for category, scripts in categorized_scripts.items():
        category_path = os.path.join(base_directory, category)
        os.makedirs(category_path, exist_ok=True)
        
        for script in scripts:
            destination = os.path.join(category_path, os.path.basename(script))
            try:
                print(f"Moving {script} to {category_path}")
                shutil.move(script, destination)
            except shutil.Error as e:
                # Overwrite the file if it already exists
                if "already exists" in str(e):
                    print(f"Overwriting existing file at {destination}")
                    os.remove(destination)
                    shutil.move(script, destination)
                else:
                    print(f"Error moving {script} to {category_path}: {e}")

# Define your actual project directory
project_dir = '/home/jacqdut/reorganized_project'

# List all scripts
print("Listing all scripts...")
all_scripts = list_scripts(project_dir)
print(f"Found {len(all_scripts)} scripts.")

# Categorize the scripts
print("Categorizing scripts...")
categorized_scripts = categorize_scripts(all_scripts)

# Move the scripts to their respective directories
print("Moving scripts to their respective directories...")
move_scripts(categorized_scripts, project_dir)
print("Script execution completed.")
