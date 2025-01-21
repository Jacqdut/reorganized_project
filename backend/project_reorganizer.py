import os
import shutil
import logging

# Initialize logging for debugging and operation tracking
logging.basicConfig(
    filename="project_reorganizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def restructure_project(root_directory, output_directory, excluded_dirs=None):
    """
    Restructure files in the project directory, skipping restricted files and logging operations.

    Parameters:
    - root_directory: The root of the original project.
    - output_directory: The directory for the reorganized project.
    - excluded_dirs: List of directories to exclude from restructuring.
    """
    excluded_dirs = excluded_dirs or []

    for root, dirs, files in os.walk(root_directory):
        # Skip excluded directories
        if any(excluded_dir in root for excluded_dir in excluded_dirs):
            logging.info(f"Skipping excluded directory: {root}")
            continue

        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(root, root_directory)
            destination_dir = os.path.join(output_directory, relative_path)
            destination_path = os.path.join(destination_dir, file)

            # Ensure the destination directory exists
            os.makedirs(destination_dir, exist_ok=True)

            try:
                # Move the file to its new location
                shutil.move(file_path, destination_path)
                logging.info(f"Moved: {file_path} -> {destination_path}")
            except PermissionError:
                logging.error(f"Permission denied for file: {file_path}. Skipping...")
            except Exception as e:
                logging.error(f"Error moving file {file_path}: {e}")

    logging.info("Restructuring completed.")


def remove_duplicates(output_directory):
    """
    Remove duplicate files based on content hash.

    Parameters:
    - output_directory: The directory where duplicates will be checked and removed.
    """
    import hashlib

    file_hashes = {}
    duplicates = []

    for root, _, files in os.walk(output_directory):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "rb") as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()

                if file_hash in file_hashes:
                    duplicates.append((file_path, file_hashes[file_hash]))
                else:
                    file_hashes[file_hash] = file_path
            except Exception as e:
                logging.error(f"Error hashing file {file_path}: {e}")

    # Remove duplicates
    for duplicate, original in duplicates:
        try:
            os.remove(duplicate)
            logging.info(
                f"Removed duplicate file: {duplicate} (Duplicate of {original})"
            )
        except Exception as e:
            logging.error(f"Error removing duplicate {duplicate}: {e}")

    logging.info("Duplicate removal completed.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Restructure and deduplicate project files."
    )
    parser.add_argument("--root", required=True, help="Root directory of the project.")
    parser.add_argument(
        "--output", required=True, help="Output directory for the reorganized project."
    )
    parser.add_argument(
        "--exclude", nargs="*", default=[], help="Directories to exclude."
    )
    args = parser.parse_args()

    print("Starting project restructuring...")
    restructure_project(args.root, args.output, args.exclude)
    print("Removing duplicates...")
    remove_duplicates(args.output)
    print(
        f"Project reorganization and duplicate removal completed. Logs saved to 'project_reorganizer.log'."
    )
