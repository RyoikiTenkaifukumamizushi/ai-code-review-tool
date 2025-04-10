import requests
import hashlib
import time
import random

API_KEY = "aa4451c8c0cf0e71c4aeea50197be433bba02571"
API_SECRET = "c111169e864ae78b386815d216a76833ab84eb7d"
CONTEST_ID = "1234"  # Replace with contest number
PROBLEM_INDEX = "A"  # Problem ID (A, B, C...)
LANGUAGE_ID = "54"  # C++17
CODE = """#include <iostream>\nusing namespace std;\nint main() {cout << "Hello, Codeforces!"; return 0;}"""

def generate_api_sig(method):
    rand = random.randint(100000, 999999)
    unix_time = str(int(time.time()))
    params = f"apiKey={API_KEY}&time={unix_time}"
    to_hash = f"{rand}/{method}?{params}#{API_SECRET}"
    hashed = hashlib.sha512(to_hash.encode()).hexdigest()
    return f"{rand}{hashed}"

def submit_solution():
    method = "contest.submit"
    sig = generate_api_sig(method)
    url = f"https://codeforces.com/api/{method}"

    payload = {
        "apiKey": API_KEY,
        "time": str(int(time.time())),
        "contestId": CONTEST_ID,
        "problemIndex": PROBLEM_INDEX,
        "programTypeId": LANGUAGE_ID,
        "source": CODE,
        "apiSig": sig,
    }

    response = requests.post(url, data=payload)
    print(response.json())

submit_solution()
