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

def extract_function_info_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source = file.read()

    tree = ast.parse(source)
    functions_info = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            analyzer = FunctionAnalyzer()
            analyzer.visit(node)

            function_info = {
                "name": node.name,
                "args": len(node.args.args),
                "lines": node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') else 0,
                "has_docstring": ast.get_docstring(node) is not None,
                "num_if": analyzer.num_if,
                "num_loops": analyzer.num_loops,
                "loop_locations": analyzer.loop_locations,
                "num_calls": analyzer.num_calls,
                "num_returns": analyzer.num_returns,
                "has_try": analyzer.has_try
            }

            functions_info.append(function_info)

    return functions_info

def extract_from_all_files(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".py"):
            file_path = os.path.join(input_folder, filename)
            print(f"Analyzing: {filename}")
            function_data = extract_function_info_from_file(file_path)

            output_filename = f"{os.path.splitext(filename)[0]}_function_info.json"
            output_path = os.path.join(output_folder, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(function_data, f, indent=4)

# Run it
if __name__ == "__main__":
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_folder = os.path.join(base_path, "examples")
    output_folder = os.path.join(base_path, "outputs")
    extract_from_all_files(input_folder, output_folder)
