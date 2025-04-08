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
        end_line = max(
            [n.lineno for n in ast.walk(node) if hasattr(n, 'lineno')],
            default=start_line
        )
        num_lines = end_line - start_line + 1

        docstring = ast.get_docstring(node)
        has_docstring = docstring is not None

        self.functions.append({
            'name': name,
            'args': arg_count,
            'lines': num_lines,
            'has_docstring': has_docstring
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

    # Extract filename only, without folder path or extension
    base_name = os.path.basename(filename)
    name_only = os.path.splitext(base_name)[0]

    # Output to 'outputs' folder
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{name_only}_function_info.json")
    with open(output_path, 'w', encoding='utf-8') as out_file:
        json.dump(extractor.functions, out_file, indent=4)

    print(f"✅ Function information written to: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python extractor/function_info_extractor.py examples/sample_code.py")
    else:
        analyze_file(sys.argv[1])
