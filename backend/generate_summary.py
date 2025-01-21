import os

log_file = "/home/jacqdut/reorganized_project/backend/project_reorganizer.log"
summary_file = "/home/jacqdut/reorganized_project/backend/reorganization_summary.txt"


def parse_log(log_file, summary_file):
    total_changes = 0
    duplicate_files = []
    error_files = []
    directory_changes = {}

    with open(log_file, "r") as log:
        for line in log:
            total_changes += 1
            if "DUPLICATE" in line:
                duplicate_files.append(line.strip())
            elif "ERROR" in line:
                error_files.append(line.strip())
            elif "MOVED" in line:
                directory = line.split("->")[-1].strip()
                directory_changes[directory] = directory_changes.get(directory, 0) + 1

    with open(summary_file, "w") as summary:
        summary.write(f"Total Changes: {total_changes}\n")
        summary.write(f"Duplicate Files Removed: {len(duplicate_files)}\n")
        summary.write(f"Errors Encountered: {len(error_files)}\n\n")
        summary.write("Directory Changes:\n")
        for directory, count in sorted(
            directory_changes.items(), key=lambda x: x[1], reverse=True
        ):
            summary.write(f"{directory}: {count} files\n")

        if duplicate_files:
            summary.write(
                "\nDuplicate Files:\n" + "\n".join(duplicate_files[:10]) + "\n..."
            )
        if error_files:
            summary.write("\nError Files:\n" + "\n".join(error_files[:10]) + "\n...")


if os.path.exists(log_file):
    parse_log(log_file, summary_file)
    print(f"Summary generated: {summary_file}")
else:
    print("Log file not found!")
