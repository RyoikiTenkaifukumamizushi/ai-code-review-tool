import google.generativeai as a
import json
import os
a.configure(api_key="AIzaSyCFAAYN7GBROF5CnurdsnSu5S8C3KxIS3I")
b=a.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
def c():
    d=os.path.dirname(__file__)
    e=os.path.join(d, "..", "new_outputs")
    f=os.path.join(d, "..", "review_results")
    os.makedirs(f, exist_ok=True)
    g=""
    for h in os.listdir(e):
        if h=="new_code_analysis.json":
            i=os.path.join(e, h)
            with open(i, "r") as j:
                k=json.load(j)
            l=f"""
You are a very helpful and experienced code reviewer bot.

I will give you an analysis of a Python file in JSON format. It includes details about functions and the expected coding style of the project.

Please compare each function to the coding standards and provide friendly, constructive feedback. Point out if anything is missing such as docstrings, logging, or try-except blocks.

Use a checklist format with ✅ or ❌ for each item per function.

JSON:
{json.dumps(k, indent=2)}
"""
            print(f"Reviewing: {h}...")
            m=b.generate_content(l)
            n=os.path.splitext(h)[0] + "_review.txt"
            o=os.path.join(f, n)
            with open(o, "w", encoding="utf-8") as p:
                p.write(m.text)
            g=m.text
            print(f"✅ Review written to: {o}")
    return g

if __name__=="__main__":
    c()
