import ast
import os
import json
class A(ast.NodeVisitor):
    def __init__(a):
        a.b=0
        a.c=0
        a.d=0
        a.e=0
        a.f=False
        a.g=[]
    def visit_If(a, b):
        a.b+=1
        a.generic_visit(b)
    def visit_For(a, b):
        a.c+=1
        a.g.append({"type": "for", "lineno": b.lineno})
        a.generic_visit(b)
    def visit_While(a, b):
        a.c+=1
        a.g.append({"type": "while", "lineno": b.lineno})
        a.generic_visit(b)
    def visit_Call(a, b):
        a.d+=1
        a.generic_visit(b)
    def visit_Return(a, b):
        a.e+=1
        a.generic_visit(b)
    def visit_Try(a, b):
        a.f=True
        a.generic_visit(b)
def B(c):
    d=1
    for e in ast.walk(c):
        if isinstance(e, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.Try, ast.ExceptHandler)):
            d+=1
    return d
def C(d, e, f):
    g=0
    for h in range(e-1, f):
        i=d[h].strip()
        if i.startswith("#"):
            g+=1
    return g
def D(e):
    with open(e, "r", encoding="utf-8") as f:
        g=f.read()
    h=g.splitlines()
    try:
        i=ast.parse(g)
    except SyntaxError as j:
        print(f"[!] Failed to parse {e}: {j}")
        return []
    k=[]
    for l in ast.walk(i):
        if isinstance(l, ast.FunctionDef):
            m=A()
            m.visit(l)
            n=l.lineno
            o=getattr(l, 'end_lineno', n + len(l.body))
            p=o-n+1
            q=C(h, n, o)
            r={
                "name": l.name,
                "args": len(l.args.args),
                "lines": p,
                "has_docstring": ast.get_docstring(l) is not None,
                "num_if": m.b,
                "num_loops": m.c,
                "loop_locations": m.g,
                "num_calls": m.d,
                "num_returns": m.e,
                "has_try": m.f,
                "cyclomatic_complexity": B(l),
                "comment_count": q,
                "comments_per_line_ratio": round(q / p, 2) if p > 0 else 0.0
            }
            k.append(r)
    return k
def E(f, g):
    os.makedirs(g, exist_ok=True)
    for h in os.listdir(f):
        if h.endswith(".py"):
            i=os.path.join(f, h)
            print(f"[+] Analyzing: {h}")
            j=D(i)
            k=f"{os.path.splitext(h)[0]}_function_info.json"
            l=os.path.join(g, k)
            with open(l, "w", encoding="utf-8") as m:
                json.dump(j, m, indent=4)
if __name__=="__main__":
    a=os.path.dirname(os.path.abspath(__file__))
    b=os.path.join(a, "..", "new_codes")
    c=os.path.join(a, "..", "new_outputs")
    b=os.path.abspath(b)
    c=os.path.abspath(c)
    E(b, c)
