import google.generativeai as genai
import json
import os

# Configure Gemini API
genai.configure(api_key="AIzaSyA3_F-cCPs-ZNuixetN463BVRqyPdWVjIk")  # Replace with your actual key

# Paths
base_dir = os.path.dirname(__file__)
json_dir = os.path.join(base_dir, "..", "new_outputs")
output_dir = os.path.join(base_dir, "..", "review_results")

# Create output folder if not exists
os.makedirs(output_dir, exist_ok=True)

# Load Gemini model
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

# Loop through all JSON files in outputs/
for file_name in os.listdir(json_dir):
    if file_name == "new_code_analysis.json":
        json_path = os.path.join(json_dir, file_name)

        # Load the JSON data
        with open(json_path, "r") as f:
            json_data = json.load(f)

        # Prepare prompt
        prompt = f"""
You are a helpful and experienced code reviewer bot.

I will give you an analysis of a Python file in JSON format. It includes details about functions and the expected coding style of the project.

Please compare each function to the coding standards and provide friendly, constructive feedback. Point out if anything is missing such as docstrings, logging, or try-except blocks.

Use a checklist format with ✅ or ❌ for each item per function.

JSON:
{json.dumps(json_data, indent=2)}
"""

        # Generate content
        print(f"Reviewing: {file_name}...")
        response = model.generate_content(prompt)

        # Write result to .txt file
        output_file = os.path.splitext(file_name)[0] + "_review.txt"
        output_path = os.path.join(output_dir, output_file)

        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(response.text)

        print(f"✅ Review written to: {output_path}")
