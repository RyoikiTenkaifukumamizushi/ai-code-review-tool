import ast
import sys
import os
import json

class FunctionInfoExtractor(ast.NodeVisitor):
    def __init__(self, source_lines):
        self.source_lines = source_lines
        self.functions = []

    def visit_FunctionDef(self, node):
        name = node.name

        arg_count = len([
            arg for arg in node.args.args
            if arg.arg not in ('self', 'cls')
        ])

        start_line = node.lineno
        end_line = max([n.lineno for n in ast.walk(node) if hasattr(n, 'lineno')], default=start_line)
        num_lines = end_line - start_line + 1

        docstring = ast.get_docstring(node)
        has_docstring = docstring is not None

        # Count features
        num_if = 0
        num_loops = 0
        num_calls = 0
        num_returns = 0
        has_try = False

        for child in ast.walk(node):
            if isinstance(child, ast.If):
                num_if += 1
            elif isinstance(child, (ast.For, ast.While)):
                num_loops += 1
            elif isinstance(child, ast.Call):
                num_calls += 1
            elif isinstance(child, ast.Return):
                num_returns += 1
            elif isinstance(child, ast.Try):
                has_try = True

        self.functions.append({
            'name': name,
            'args': arg_count,
            'lines': num_lines,
            'has_docstring': has_docstring,
            'num_if': num_if,
            'num_loops': num_loops,
            'num_calls': num_calls,
            'num_returns': num_returns,
            'has_try': has_try
        })

        self.generic_visit(node)


def analyze_file(filename):
    if not os.path.isfile(filename):
        print(f"❌ File not found: {filename}")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
        source_lines = source.splitlines()

    tree = ast.parse(source, filename=filename)
    extractor = FunctionInfoExtractor(source_lines)
    extractor.visit(tree)

    # Ensure the outputs directory exists
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_filename = os.path.join(output_dir, f'{base_name}_function_info.json')

    with open(output_filename, 'w', encoding='utf-8') as out_file:
        json.dump(extractor.functions, out_file, indent=4)

    print(f"✅ Function information written to: {output_filename}")


# Command-line usage
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python function_info_extractor.py <filename.py>")
    else:
        analyze_file(sys.argv[1])
