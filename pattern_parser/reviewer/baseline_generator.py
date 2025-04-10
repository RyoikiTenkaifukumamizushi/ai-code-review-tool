import os
import json
def A(B):
    C=[]
    for D in os.listdir(B):
        if D.endswith("_function_info.json"):
            E=os.path.join(B, D)
            with open(E, "r", encoding="utf-8") as F:
                G=json.load(F)
                C.extend(G)
    return C
def H(I):
    J=K=L=M=N=O=P=0
    for Q in I:
        J+=Q.get("lines", 0)
        K+=Q.get("num_if", 0)
        L+=Q.get("num_loops", 0)
        M+=Q.get("num_calls", 0)
        N+=Q.get("num_returns", 0)
        O+=1 if Q.get("has_try") else 0
        P+=Q.get("num_comments", 0)
    R=len(I) or 1
    S={
        "function_count": len(I),
        "avg_lines": J/R,
        "avg_if": K/R,
        "avg_loops": L/R,
        "avg_calls": M/R,
        "avg_returns": N/R,
        "avg_comments": P/R,
        "try_block_ratio": O/R
    }
    return S
def T(U, V):
    with open(U, "w", encoding="utf-8") as W:
        json.dump(V, W, indent=4)
    print(f"✅ Baseline metrics saved to: {U}")
if __name__=="__main__":
    X=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    Y=os.path.join(X, "outputs")
    Z=os.path.join(X, "outputs", "baseline.json")
    print(f"📊 Generating baseline from folder: {Y}")
    a=A(Y)
    b=H(a)
    T(Z, b)
