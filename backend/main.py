from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import UploadFile, Form
import os
import shutil
import subprocess
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/download-review/")
def download_review():
    # Get absolute path to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "pattern_parser", "review_results", "new_code_analysis_review.txt")

    print(f"Looking for review file at: {file_path}")  # <--- Add this line

    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename="code_review.txt",
            media_type='text/plain'
        )
    return {"error": "Review file not found"}
@app.post("/submit/")
async def submit_code(code: str = Form(None), file: UploadFile = None):
    base_dir = os.path.dirname(__file__)
    parser_root = os.path.abspath(os.path.join(base_dir, "..", "pattern_parser"))
    new_codes_dir = os.path.join(parser_root, "new_codes")
    pasted_path = os.path.join(new_codes_dir, "pasted_code.py")

    # Ensure folder exists
    os.makedirs(new_codes_dir, exist_ok=True)

    # Determine input source: file or pasted code
    if file:
        content = await file.read()
        code_str = content.decode("utf-8")
    elif code:
        code_str = code
    else:
        return "❌ No code or file submitted"

    # Clean up line endings and write to pasted_code.py
    cleaned_code = "\n".join(line.rstrip() for line in code_str.replace('\r\n', '\n').split('\n'))
    with open(pasted_path, "w", encoding="utf-8") as f:
        f.write(cleaned_code)

    # Optional: delete all other .py files except pasted_code.py
    for fname in os.listdir(new_codes_dir):
        fpath = os.path.join(new_codes_dir, fname)
        if fname.endswith(".py") and fname != "pasted_code.py":
            os.remove(fpath)

    # Run the analysis pipeline
    subprocess.run(["python", os.path.join(parser_root, "extractor", "function_info_extractor.py")])
    subprocess.run(["python", os.path.join(parser_root, "reviewer", "new_code_analyzer.py")])
    subprocess.run(["python", os.path.join(parser_root, "reviewer", "reviewer.py")])

    # Return review result
    result_path = os.path.join(parser_root, "review_results", "new_code_analysis_review.txt")
    if os.path.exists(result_path):
        with open(result_path, "r", encoding="utf-8") as review_file:
            return review_file.read()
    else:
        return "❌ Review file not generated."