import json


# Function to generate a list of 2048 floating-point values
def generate_image_features():
    return [round(i * 0.1, 1) for i in range(1, 2049)]


# Example data
data = [
    {
        "image_features": generate_image_features(),
        "question": "What is in the image?",
        "answer": 1,
    },
    {
        "image_features": generate_image_features(),
        "question": "What is the color of the object?",
        "answer": 2,
    },
]

# Write data to a JSON file
with open("/home/jacqdut/reorganized_project/data/vqa_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("JSON data file generated successfully.")
