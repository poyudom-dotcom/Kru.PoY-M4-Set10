import os
import subprocess

TEST_CASES = {
    "Examination_1": [
        {"input": "130\n", "expected": "2\n10"},
        {"input": "45\n", "expected": "0\n45"}
    ],
    "Examination_2": [
        {"input": "10\n5\n", "expected": "A is greater"},
        {"input": "3\n8\n", "expected": "B is greater or equal"},
        {"input": "5\n5\n", "expected": "B is greater or equal"}
    ],
    "Examination_3": [
        {"input": "12345678\n", "expected": "Pass"},
        {"input": "abc\n", "expected": "Too Short"}
    ],
    "Examination_4": [
        {"input": "red\n", "expected": "Stop"},
        {"input": "yellow\n", "expected": "Slow"},
        {"input": "green\n", "expected": "Go"},
        {"input": "blue\n", "expected": "Invalid"}
    ],
    "Examination_5": [
        {"input": "40\n", "expected": "120"},
        {"input": "80\n", "expected": "320"},
        {"input": "120\n", "expected": "600"}
    ]
}

def is_equal(actual, expected):
    clean_actual = actual.strip().lower()
    clean_expected = expected.strip().lower()
    
    if clean_actual == clean_expected:
        return True
        
    try:
        if float(clean_actual) == float(clean_expected):
            return True
    except ValueError:
        pass
        
    return False

def run_tests():
    all_passed = True
    
    for file_name, cases in TEST_CASES.items():
        py_file = f"{file_name}.py"
        if not os.path.exists(py_file):
            continue

        print(f"\n--- Testing {py_file} ---")
        for i, case in enumerate(cases, 1):
            try:
                process = subprocess.Popen(
                    ["python", py_file],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5
                )
                stdout, stderr = process.communicate(input=case["input"])
                
                if is_equal(stdout, case["expected"]):
                    print(f"  Test Case {i}: PASSED ✅")
                else:
                    got_clean = stdout.strip()
                    print(f"  Test Case {i}: FAILED ❌ (Got: '{got_clean}', Expected: '{case['expected']}')")
                    all_passed = False
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"  Test Case {i}: FAILED ❌ (Timeout - โค้ดติด Infinite Loop)")
                all_passed = False
            except Exception as e:
                print(f"  Test Case {i}: ERROR ❌ ({str(e)})")
                all_passed = False

    if not all_passed:
        exit(1)

if __name__ == "__main__":
    run_tests()
