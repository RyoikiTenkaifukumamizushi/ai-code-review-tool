# 🤖 AI Code Review Tool

This project is a collaborative tool that parses Python code, extracts function metadata, and uses AI (via OpenAI API) to generate reviews and suggestions for improvement.

## 📌 Project Overview

The tool is divided among 4 contributors, each with a specific role:

- **🔹 Person 1 (You)** – Function info extractor (AST-based parser)
- **🔹 Person 2** – Processes extracted JSON data (summarizer/statistics builder)
- **🔹 Person 3** – Prompt engineer (uses OpenAI API to generate code reviews)
- **🔹 Person 4** – UI engineer (frontend or backend to present the output)

---

## 🧱 Folder Structure
ai-code-review-tool/
│
├── extractor/                 
│   └── function_info_extractor.py ← AST-based feature extraction logic
|   └── example_codes/             ← Input sample Python code files
│	├── outputs/                   ← JSON files with extracted function info
|    ── run_all.bat                ← Runs parser for all files in example_codes/
│
├── analyzer/                  ← (To be created by Person 2)
│   └── pattern_comparator.py
│
├── new_code/                  ← New code to be analyzed
│
└── README.md                  ← You're here!

Output will be stored in outputs/sample_code_function_info.json.

You can also run all files inside examples/:
.\run_all.bat
🔄 Step 2: Process JSON Data (Person 2)
Consumes the output JSON files and extracts summaries/statistics (like most used functions, longest ones, etc.).
🧠 Step 3: AI Code Review (Person 3)
Uses OpenAI API with custom prompts based on function metadata to generate helpful suggestions for each function.
🎨 Step 4: UI Integration (Person 4)
Builds a UI (CLI, Web, or App) to display the results in a human-readable way.

🧑‍💻 Contributing
Each person works in their assigned folder and commits code regularly. Follow these conventions:

Use meaningful commit messages.

Keep all raw code examples in examples/.

Outputs from Person 1 go in extractor/outputs/.

