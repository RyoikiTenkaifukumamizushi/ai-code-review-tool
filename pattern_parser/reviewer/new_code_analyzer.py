import os
import json

THRESHOLD_FACTOR = 1.5  # Flag if attribute is 1.5x more than the baseline

def load_baseline(baseline_path):
    with open(baseline_path, "r", encoding="utf-8") as f:
        return json.load(f)

def analyze_function_against_baseline(func, baseline):
    alerts = []

    if func["lines"] > baseline["avg_lines"] * THRESHOLD_FACTOR:
        alerts.append(f"Too many lines ({func['lines']} > avg {baseline['avg_lines']:.2f})")
    
    if func["num_if"] > baseline["avg_if"] * THRESHOLD_FACTOR:
        alerts.append(f"Too many if-statements ({func['num_if']})")
    
    if func["num_loops"] > baseline["avg_loops"] * THRESHOLD_FACTOR:
        alerts.append(f"Too many loops ({func['num_loops']})")
    
    if func["num_calls"] > baseline["avg_calls"] * THRESHOLD_FACTOR:
        alerts.append(f"Too many function calls ({func['num_calls']})")
    
    if func["num_returns"] > baseline["avg_returns"] * THRESHOLD_FACTOR:
        alerts.append(f"Too many return statements ({func['num_returns']})")

    if func.get("num_comments", 0) < baseline["avg_comments"] * 0.5:
        alerts.append("Too few comments")

    if not func.get("has_docstring", False):
        alerts.append("Missing docstring")

    if not func.get("has_try", False):
        alerts.append("No try block (baseline ratio: {:.2f})".format(baseline["try_block_ratio"]))

    return alerts

def analyze_file(file_path, baseline):
    with open(file_path, "r", encoding="utf-8") as f:
        functions = json.load(f)

    results = []
    for func in functions:
        issues = analyze_function_against_baseline(func, baseline)
        results.append({
            "function": func["name"],
            "issues": issues
        })
    return results

def analyze_folder(folder_path, baseline_path):
    baseline = load_baseline(baseline_path)
    flagged_results = {}

    for filename in os.listdir(folder_path):
        if filename.endswith("_function_info.json"):
            file_path = os.path.join(folder_path, filename)
            print(f"🔍 Analyzing {filename}")
            analysis = analyze_file(file_path, baseline)
            flagged_results[filename] = analysis

    return flagged_results

def save_analysis(output_path, analysis):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=4)
    print(f"✅ Analysis saved to: {output_path}")

# Run it
if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))

    input_folder = os.path.join(base_path, "..", "new_outputs")
    baseline_file = os.path.join(base_path, "..", "outputs", "baseline.json")
    output_file = os.path.join(base_path, "..", "new_outputs", "new_code_analysis.json")

    results = analyze_folder(os.path.abspath(input_folder), os.path.abspath(baseline_file))
    save_analysis(os.path.abspath(output_file), results)
