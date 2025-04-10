from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import subprocess
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/submit/")
async def submit_code(code: str = Form(None), file: UploadFile = None):
    base_dir = os.path.dirname(__file__)
    parser_root = os.path.abspath(os.path.join(base_dir, "..", "pattern_parser"))
    new_codes_dir = os.path.join(parser_root, "new_codes")
    if code:
    # Normalize line endings and remove trailing spaces
        cleaned_code = "\n".join(line.rstrip() for line in code.replace('\r\n', '\n').split('\n'))
        with open(os.path.join(new_codes_dir, "pasted_code.py"), "w", encoding="utf-8") as f:
            f.write(cleaned_code)

    if file:
        file_path = os.path.join(new_codes_dir, file.filename)
        with open(file_path, "wb") as f_out:
            shutil.copyfileobj(file.file, f_out)



    # 2. Run function_info_extractor to generate JSONs
    subprocess.run(["python", os.path.join(parser_root, "extractor", "function_info_extractor.py")])
    subprocess.run(["python", os.path.join(parser_root, "reviewer", "new_code_analyzer.py")])
    subprocess.run(["python", os.path.join(parser_root, "reviewer", "reviewer.py")])
    result_path = os.path.join(parser_root, "review_results", "new_code_analysis_review.txt")
    if os.path.exists(result_path):
        with open(result_path, "r", encoding="utf-8") as review_file:
            return review_file.read()
    else:
        return "❌ Review file not generated."
