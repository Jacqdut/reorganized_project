import os
import hashlib

def hash_file(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_duplicates(directory):
    file_hashes = {}
    duplicates = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hash_file(file_path)
            if file_hash in file_hashes:
                duplicates.append((file_hashes[file_hash], file_path))
            else:
                file_hashes[file_hash] = file_path

    return duplicates

# Search for duplicates in the 'reorganized_project' directory
duplicates = find_duplicates('/home/jacqdut/reorganized_project')
for original, duplicate in duplicates:
    print(f"Duplicate found: {duplicate} (original: {original})")
