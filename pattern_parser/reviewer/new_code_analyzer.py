import os
import ast
import json
A=1.5
B=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "new_codes"))
def C(D):
    E=os.path.basename(D).replace("_function_info.json", ".py")
    F=os.path.join(B, E)
    if not os.path.exists(F):
        return{"error": f"Python file not found: {F}"}
    try:
        with open(F, "r", encoding="utf-8") as G:
            H=G.read()
        ast.parse(H)
        return None
    except SyntaxError as I:
        return{
            "message": str(I),
            "line": I.lineno,
            "offset": I.offset,
            "text": I.text.strip() if I.text else ""
        }

def J(K):
    with open(K, "r", encoding="utf-8") as L:
        return json.load(L)

def M(N, O):
    P=[]
    if N["lines"]>O["avg_lines"]:
        P.append(f"❗ Too many lines ({N['lines']} > avg {O['avg_lines']:.2f})")
    else:
        P.append(f"✅ Number of lines is within range ({N['lines']} ≤ {O['avg_lines'] * A:.2f})")

    if N["num_if"]>O["avg_if"]:
        P.append(f"❗ Too many if-statements ({N['num_if']})")
    else:
        P.append(f"✅ If-statements count is within range ({N['num_if']})")
    if N["num_loops"]>O["avg_loops"]:
        P.append(f"❗ Too many loops ({N['num_loops']})")
    else:
        P.append(f"✅ Loop usage is within range ({N['num_loops']})")
    if N["num_calls"]>O["avg_calls"]:
        P.append(f"❗ Too many function calls ({N['num_calls']})")
    else:
        P.append(f"✅ Function calls are within range ({N['num_calls']})")
    if N["num_returns"]>O["avg_returns"]:
        P.append(f"❗ Too many return statements ({N['num_returns']})")
    else:
        P.append(f"✅ Return statement count is within range ({N['num_returns']})")
    if N.get("num_comments", 0)<O["avg_comments"] * 0.5:
        P.append("❗ Too few comments")
    else:
        P.append("✅ Adequate number of comments")
    if not N.get("has_docstring", False):
        P.append("❗ Missing docstring")
    else:
        P.append("✅ Docstring is present")
    if not N.get("has_try", False):
        P.append("❗ No try block (baseline ratio: {:.2f})".format(O["try_block_ratio"]))
    else:
        P.append("✅ Try-except block is present")
    return P
def Q(R, S):
    with open(R, "r", encoding="utf-8") as T:
        U=json.load(T)
    V=[]
    for W in U:
        X=M(W, S)
        V.append({
            "function": W["name"],
            "issues": X
        })
    return V
def Y(Z, a):
    b=J(a)
    c={}
    for d in os.listdir(Z):
        if d.endswith("_function_info.json"):
            e=os.path.join(Z, d)
            f=C(e)
            g={
                "file": d.replace("_function_info.json", ".py"),
                "syntax": "✅ No syntax errors found"
            }
            if f:
                g["syntax"]=f"❗ Syntax error on line {f['line']}: {f['message']}"
                g["code"]=f["text"]
            print(f"🔍 Analyzing {d}")
            h=Q(e, b)
            c[d]={
                "syntax_check": g,
                "functions": h
            }
    return c
def i(j, k):
    with open(j, "w", encoding="utf-8") as l:
        json.dump(k, l, indent=4)
    print(f"✅ Analysis saved to: {j}")
if __name__=="__main__":
    m=os.path.dirname(os.path.abspath(__file__))
    n=os.path.join(m, "..", "new_outputs")
    o=os.path.join(m, "..", "outputs", "baseline.json")
    p=os.path.join(m, "..", "new_outputs", "new_code_analysis.json")
    q=Y(os.path.abspath(n), os.path.abspath(o))
    i(os.path.abspath(p), q)
