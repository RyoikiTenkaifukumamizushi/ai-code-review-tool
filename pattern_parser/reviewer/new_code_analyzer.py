import os
import ast
import json
THRESHOLD_FACTOR=1.5  
PY_CODE_FOLDER=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "new_codes"))
def check_syntax(json_path):
    py_filename=os.path.basename(json_path).replace("_function_info.json", ".py")
    py_path=os.path.join(PY_CODE_FOLDER, py_filename)
    if not os.path.exists(py_path):
        return{"error": f"Python file not found: {py_path}"}
    try:
        with open(py_path, "r", encoding="utf-8") as f:
            source=f.read()
        ast.parse(source)
        return None  
    except SyntaxError as e:
        return{
            "message": str(e),
            "line": e.lineno,
            "offset": e.offset,
            "text": e.text.strip() if e.text else ""
        }
def load_baseline(baseline_path):
    with open(baseline_path, "r", encoding="utf-8") as f:
        return json.load(f)
def analyze_function_against_baseline(func, baseline):
    alerts = []
    if func["lines"] > baseline["avg_lines"] * THRESHOLD_FACTOR:
        alerts.append(f"❗ Too many lines ({func['lines']}>avg {baseline['avg_lines']:.2f})")
    else:
        alerts.append(f"✅ Number of lines is within range ({func['lines']} ≤ {baseline['avg_lines'] * THRESHOLD_FACTOR:.2f})")
    if func["num_if"] > baseline["avg_if"] * THRESHOLD_FACTOR:
        alerts.append(f"❗ Too many if-statements ({func['num_if']})")
    else:
        alerts.append(f"✅ If-statements count is within range ({func['num_if']})")
    if func["num_loops"] > baseline["avg_loops"] * THRESHOLD_FACTOR:
        alerts.append(f"❗ Too many loops ({func['num_loops']})")
    else:
        alerts.append(f"✅ Loop usage is within range ({func['num_loops']})")
    if func["num_calls"] > baseline["avg_calls"] * THRESHOLD_FACTOR:
        alerts.append(f"❗ Too many function calls ({func['num_calls']})")
    else:
        alerts.append(f"✅ Function calls are within range ({func['num_calls']})")
    if func["num_returns"] > baseline["avg_returns"] * THRESHOLD_FACTOR:
        alerts.append(f"❗ Too many return statements ({func['num_returns']})")
    else:
        alerts.append(f"✅ Return statement count is within range ({func['num_returns']})")
    if func.get("num_comments", 0) < baseline["avg_comments"] * 0.5:
        alerts.append("❗ Too few comments")
    else:
        alerts.append("✅ Adequate number of comments")
    if not func.get("has_docstring", False):
        alerts.append("❗ Missing docstring")
    else:
        alerts.append("✅ Docstring is present")
    if not func.get("has_try", False):
        alerts.append("❗ No try block (baseline ratio: {:.2f})".format(baseline["try_block_ratio"]))
    else:
        alerts.append("✅ Try-except block is present")
    return alerts


def analyze_file(file_path, baseline):
    with open(file_path, "r", encoding="utf-8") as f:
        functions=json.load(f)
    results = []
    for func in functions:
        issues=analyze_function_against_baseline(func, baseline)
        results.append({
            "function": func["name"],
            "issues": issues
        })
    return results

def analyze_folder(folder_path, baseline_path):
    baseline=load_baseline(baseline_path)
    flagged_results={}
    for filename in os.listdir(folder_path):
        if filename.endswith("_function_info.json"):
            file_path=os.path.join(folder_path, filename)
            syntax_issue=check_syntax(file_path)
            syntax_result={
                "file": filename.replace("_function_info.json", ".py"),
                "syntax": "✅ No syntax errors found"
            }
            if syntax_issue:
                syntax_result["syntax"]=f"❗ Syntax error on line {syntax_issue['line']}: {syntax_issue['message']}"
                syntax_result["code"]=syntax_issue["text"]
            print(f"🔍 Analyzing {filename}")
            analysis=analyze_file(file_path, baseline)
            flagged_results[filename]={
                "syntax_check": syntax_result,
                "functions": analysis
            }
    return flagged_results
def save_analysis(output_path, analysis):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=4)
    print(f"✅ Analysis saved to: {output_path}")
if __name__ == "__main__":
    base_path=os.path.dirname(os.path.abspath(__file__))
    input_folder=os.path.join(base_path, "..", "new_outputs")
    baseline_file=os.path.join(base_path, "..", "outputs", "baseline.json")
    output_file=os.path.join(base_path, "..", "new_outputs", "new_code_analysis.json")
    results=analyze_folder(os.path.abspath(input_folder), os.path.abspath(baseline_file))
    save_analysis(os.path.abspath(output_file), results)
