import google.generativeai as genai
import json
import os
# BOMBARIRO CROCODILO
genai.configure(api_key="AIzaSyB2Sfec6QJ-e_2yCCinG5lP2o-IqAv8lQI")  
model=genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
def run_review():
    base_dir=os.path.dirname(__file__)
    json_dir=os.path.join(base_dir, "..", "new_outputs")
    output_dir=os.path.join(base_dir, "..", "review_results")
    os.makedirs(output_dir, exist_ok=True)
    review_output=""  
    for file_name in os.listdir(json_dir):
        if file_name=="new_code_analysis.json":
            json_path=os.path.join(json_dir, file_name)
            with open(json_path, "r") as f:
                json_data = json.load(f)
            prompt = f"""
You are a very helpful and experienced code reviewer bot.

I will give you an analysis of a Python file in JSON format. It includes details about functions and the expected coding style of the project.

Please compare each function to the coding standards and provide friendly, constructive feedback. Point out if anything is missing such as docstrings, logging, or try-except blocks.

Use a checklist format with ✅ or ❌ for each item per function.

JSON:
{json.dumps(json_data, indent=2)}
"""
            print(f"Reviewing: {file_name}...")
            response = model.generate_content(prompt)
            output_file = os.path.splitext(file_name)[0] + "_review.txt"
            output_path = os.path.join(output_dir, output_file)
            with open(output_path, "w", encoding="utf-8") as out_file:
                out_file.write(response.text)
            review_output = response.text
            print(f"✅ Review written to: {output_path}")
    return review_output
#TRALALERO TRALALA
if __name__ == "__main__":
    run_review()
