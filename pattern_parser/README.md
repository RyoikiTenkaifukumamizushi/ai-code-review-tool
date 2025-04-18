# 🧠 AI Code Review Tool 🔍

This is a Python-based tool that analyzes Python functions and uses **Gemini AI** to generate friendly, constructive code reviews based on coding standards.

---

## 📂 Project Structure

ai-code-review-tool/ 
├── analyzer/ # Code analyzer module (optional for now) 
├── pattern_parser/ 
│ ├── extractor/ # Parses and extracts function-level info 
│ ├── outputs/ # Baseline JSON outputs 
│ ├── new_codes/ # Your new code files to analyze 
│ ├── new_outputs/ # Function info extracted from new code 
│ ├── reviewer/ # Gemini-powered code review script 
│ └── review_results/ # Final review outputs (.txt files) 
├── prompts/ # Prompt templates (optional) 
├── ui/ # (Optional) Frontend for interacting with the tool 
└── README.md # This file


---

## ⚙️ How It Works

1. **Extract function info** from your new code into `new_outputs/` (using your `function_analysis.py` or similar).
2. **Compare** each function to your `outputs/` (baseline).
3. **Review** it using Gemini via `reviewer.py`.

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install google-generativeai
2. Add your Gemini API Key
In reviewer.py:

genai.configure(api_key="YOUR_API_KEY_HERE")
🔒 Keep this key private! Do not commit it to public repositories.

3. Run the Review
cd pattern_parser/reviewer
python reviewer.py
Reviews will be saved in the review_results/ folder.

📝 Output Example
✅ Review written to: review_results/new_code_analysis_review.txt
Each review provides:

✅/❌ Checklist for best practices

Suggestions for refactoring

Comments on docstrings, loops, if-conditions, etc.

📌 Notes
The baseline data should already be present in outputs/.

The new code to review should be analyzed into JSON format first and placed in new_outputs/.

Reviews are generated per function, so it's very granular.

🤝 Contributing
This is a hackathon-style project. Feel free to fork or extend it with:

Web UI

Better baseline learning

Integration with GitHub PRs