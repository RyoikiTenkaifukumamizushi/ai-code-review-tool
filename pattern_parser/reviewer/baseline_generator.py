import os
import json
def load_all_function_data(folder_path):
    all_functions=[]
    for filename in os.listdir(folder_path):
        if filename.endswith("_function_info.json"):
            file_path=os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data=json.load(f)
                all_functions.extend(data)
    return all_functions
def compute_baseline_metrics(functions):
    total_lines=total_if=total_loops=total_calls=total_returns=total_try=total_comments=0
    for func in functions:
        total_lines+=func.get("lines", 0)
        total_if+=func.get("num_if", 0)
        total_loops+=func.get("num_loops", 0)
        total_calls+=func.get("num_calls", 0)
        total_returns+=func.get("num_returns", 0)
        total_try+=1 if func.get("has_try") else 0
        total_comments+=func.get("num_comments", 0)
    count=len(functions) or 1  
    baseline={
        "function_count": len(functions),
        "avg_lines": total_lines/count,
        "avg_if": total_if/count,
        "avg_loops": total_loops/count,
        "avg_calls": total_calls/count,
        "avg_returns": total_returns/count,
        "avg_comments": total_comments/count,
        "try_block_ratio": total_try/count
    }
    return baseline
def save_baseline(output_path, baseline_metrics):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(baseline_metrics, f, indent=4)
    print(f"✅ Baseline metrics saved to: {output_path}")
if __name__ == "__main__":
    base_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_folder=os.path.join(base_path, "outputs")
    output_file=os.path.join(base_path, "outputs", "baseline.json")
    print(f"📊 Generating baseline from folder: {input_folder}")
    all_functions=load_all_function_data(input_folder)
    baseline=compute_baseline_metrics(all_functions)
    save_baseline(output_file, baseline)
