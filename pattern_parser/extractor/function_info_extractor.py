import ast
import os
import json

class FunctionAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.num_if = 0
        self.num_loops = 0
        self.num_calls = 0
        self.num_returns = 0
        self.has_try = False
        self.loop_locations = []

    def visit_If(self, node):
        self.num_if += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.num_loops += 1
        self.loop_locations.append({"type": "for", "lineno": node.lineno})
        self.generic_visit(node)

    def visit_While(self, node):
        self.num_loops += 1
        self.loop_locations.append({"type": "while", "lineno": node.lineno})
        self.generic_visit(node)

    def visit_Call(self, node):
        self.num_calls += 1
        self.generic_visit(node)

    def visit_Return(self, node):
        self.num_returns += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.has_try = True
        self.generic_visit(node)

def calculate_cyclomatic_complexity(node):
    """
    Cyclomatic Complexity = 1 + number of decision points (if, for, while, try, etc.)
    """
    complexity = 1
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.Try, ast.ExceptHandler)):
            complexity += 1
    return complexity

def count_comments_in_function(source_lines, start_lineno, end_lineno):
    comment_count = 0
    for i in range(start_lineno - 1, end_lineno):
        stripped = source_lines[i].strip()
        if stripped.startswith("#"):
            comment_count += 1
    return comment_count

def extract_function_info_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source = file.read()

    source_lines = source.splitlines()
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"[!] Failed to parse {file_path}: {e}")
        return []

    functions_info = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            analyzer = FunctionAnalyzer()
            analyzer.visit(node)

            start_lineno = node.lineno
            end_lineno = getattr(node, 'end_lineno', start_lineno + len(node.body))

            total_lines = end_lineno - start_lineno + 1
            comment_count = count_comments_in_function(source_lines, start_lineno, end_lineno)

            function_info = {
                "name": node.name,
                "args": len(node.args.args),
                "lines": total_lines,
                "has_docstring": ast.get_docstring(node) is not None,
                "num_if": analyzer.num_if,
                "num_loops": analyzer.num_loops,
                "loop_locations": analyzer.loop_locations,
                "num_calls": analyzer.num_calls,
                "num_returns": analyzer.num_returns,
                "has_try": analyzer.has_try,
                "cyclomatic_complexity": calculate_cyclomatic_complexity(node),
                "comment_count": comment_count,
                "comments_per_line_ratio": round(comment_count / total_lines, 2) if total_lines > 0 else 0.0
            }

            functions_info.append(function_info)

    return functions_info

def extract_from_all_files(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".py"):
            file_path = os.path.join(input_folder, filename)
            print(f"[+] Analyzing: {filename}")
            function_data = extract_function_info_from_file(file_path)

            output_filename = f"{os.path.splitext(filename)[0]}_function_info.json"
            output_path = os.path.join(output_folder, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(function_data, f, indent=4)

if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))  # Not dirname(dirname(...))
    input_folder = os.path.join(base_path, "..", "examples")
    output_folder = os.path.join(base_path, "..", "outputs")
    input_folder = os.path.abspath(input_folder)
    output_folder = os.path.abspath(output_folder)

    extract_from_all_files(input_folder, output_folder)