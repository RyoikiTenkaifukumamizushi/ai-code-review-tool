from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.responses import JSONResponse
import os
import shutil
import subprocess
import time
import glob

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/history/")
def get_history():
    base_dir = os.path.join(os.path.dirname(__file__), "../pattern_parser/history")
    base_dir = os.path.abspath(base_dir)  # Get absolute path

    os.makedirs(base_dir, exist_ok=True)

    session_folders = sorted(os.listdir(base_dir), reverse=True)
    history_data = []

    for folder in session_folders:
        folder_path = os.path.join(base_dir, folder)
        code_file = None
        review_file = None

        for file in os.listdir(folder_path):
            if file.endswith(".py"):
                code_file = os.path.join(folder_path, file)
            elif file.endswith(".txt"):
                review_file = os.path.join(folder_path, file)

        if code_file and review_file:
            with open(code_file, "r", encoding="utf-8") as f:
                code = f.read()
            with open(review_file, "r", encoding="utf-8") as f:
                review = f.read()

            history_data.append({
                "timestamp": folder.replace("session_", ""),
                "code": code,
                "review": review
            })

    return history_data

@app.get("/download-review/")
def download_review():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "pattern_parser", "review_results", "new_code_analysis_review.txt")
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename="code_review.txt",
            media_type='text/plain'
        )
    return {"error": "Review file not found"}

@app.post("/submit/", response_class=PlainTextResponse)
async def submit_code(code: str = Form(None), file: UploadFile = None):
    base_dir = os.path.dirname(__file__)
    parser_root = os.path.abspath(os.path.join(base_dir, "..", "pattern_parser"))
    new_codes_dir = os.path.join(parser_root, "new_codes")
    pasted_path = os.path.join(new_codes_dir, "pasted_code.py")
    review_result_path = os.path.join(parser_root, "review_results", "new_code_analysis_review.txt")

    # Ensure folders exist
    os.makedirs(new_codes_dir, exist_ok=True)

    # Determine input source
    if file:
        content = await file.read()
        code_str = content.decode("utf-8")
    elif code:
        code_str = code
    else:
        return "❌ No code or file submitted"

    # Normalize and save pasted code
    cleaned_code = "\n".join(line.rstrip() for line in code_str.replace('\r\n', '\n').split('\n'))
    with open(pasted_path, "w", encoding="utf-8") as f:
        f.write(cleaned_code)

    # Delete any other Python files
    for fname in os.listdir(new_codes_dir):
        fpath = os.path.join(new_codes_dir, fname)
        if fname.endswith(".py") and fname != "pasted_code.py":
            os.remove(fpath)

    # Run pipeline
    subprocess.run(["python", os.path.join(parser_root, "extractor", "function_info_extractor.py")])
    subprocess.run(["python", os.path.join(parser_root, "reviewer", "new_code_analyzer.py")])
    subprocess.run(["python", os.path.join(parser_root, "reviewer", "reviewer.py")])

    # Check and save review
    if os.path.exists(review_result_path):
        with open(review_result_path, "r", encoding="utf-8") as review_file:
            review_text = review_file.read()

        # Save to history
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        history_dir = os.path.join(parser_root, "history", f"session_{timestamp}")
        os.makedirs(history_dir, exist_ok=True)
        with open(os.path.join(history_dir, "submitted_code.py"), "w", encoding="utf-8") as code_file:
            code_file.write(cleaned_code)
        with open(os.path.join(history_dir, "review.txt"), "w", encoding="utf-8") as review_out:
            review_out.write(review_text)

        return review_text
    else:
        return "❌ Review file not generated."
