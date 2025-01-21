import os

# Define the old and new paths
OLD_PATH = "/home/jacqdut/combined_project"
NEW_PATH = "/home/jacqdut/combined_project"

# List of file extensions to check for old paths
FILE_EXTENSIONS = [".txt", ".json", ".py", ".js", ".env"]


# Function to replace old paths with new paths in a file
def replace_paths_in_file(file_path, old_path, new_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()

        if old_path in content:
            updated_content = content.replace(old_path, new_path)
            with open(file_path, "w") as file:
                file.write(updated_content)
            print(f"Updated paths in: {file_path}")
        else:
            print(f"No updates needed in: {file_path}")
    except Exception as e:
        print(f"Error updating {file_path}: {e}")


# Function to recursively search for files and replace paths
def update_paths_in_directory(directory, old_path, new_path, file_extensions):
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                replace_paths_in_file(file_path, old_path, new_path)


# Start the path replacement process
def main():
    directory_to_scan = "/home/jacqdut/combined_project"
    print(f"Starting path replacement in directory: {directory_to_scan}")
    update_paths_in_directory(directory_to_scan, OLD_PATH, NEW_PATH, FILE_EXTENSIONS)
    print("Path replacement completed.")


if __name__ == "__main__":
    main()
