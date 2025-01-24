import os

required_directories = [
    'data',
    'models',
    'scripts',
    'tests',
    'docs'
]

project_path = '/home/jacqdut/reorganized_project'

for directory in required_directories:
    dir_path = os.path.join(project_path, directory)
    if not os.path.exists(dir_path):
        print(f"Missing directory: {dir_path}")
    else:
        print(f"Directory exists: {dir_path}")
