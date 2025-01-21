import os
import openai

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

# Define the directory to analyze
PROJECT_DIR = "/home/jacqdut/reorganized_project"

def read_file(file_path):
    """Reads a file and returns its content."""
    with open(file_path, "r") as file:
        return file.read()

def analyze_code(file_content):
    """Uses OpenAI's ChatCompletion endpoint to analyze code."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert code analyzer."},
                {"role": "user", "content": f"Analyze this code for issues and suggest improvements:\n\n{file_content}"}
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error during analysis: {str(e)}"

def process_files(directory):
    """Processes all Python files in the given directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Analyzing {file_path}...")
                try:
                    file_content = read_file(file_path)
                    analysis_result = analyze_code(file_content)
                    print(f"\n--- Analysis for {file} ---\n{analysis_result}\n")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

if __name__ == "__main__":
    process_files(PROJECT_DIR)
