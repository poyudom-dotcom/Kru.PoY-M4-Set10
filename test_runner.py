import sys
import os
import subprocess

# ==============================================================================
# ⚙️ ชุดทดสอบข้อสอบทั้ง 5 ข้อสำหรับ Kru.PoY-M4-Set10 (ข้อละ 4 เคส = ข้อละ 4 คะแนน)
# ==============================================================================
EXAM_TEST_CASES = {
    # ข้อ 1: แปลงนาทีเป็นชั่วโมงและนาที (บรรทัด 1: ชั่วโมง, บรรทัด 2: นาที)
    "Examination_1.py": [
        (["130"], "2\n10"),
        (["45"], "0\n45"),
        (["180"], "3\n0"),
        (["0"], "0\n0")
    ],
    # ข้อ 2: เปรียบเทียบตัวเลข 2 จำนวน (A > B: A is greater, A <= B: B is greater or equal)
    "Examination_2.py": [
        (["10", "5"], "A is greater"),
        (["5", "10"], "B is greater or equal"),
        (["7", "7"], "B is greater or equal"),
        (["100", "-5"], "A is greater")
    ],
    # ข้อ 3: ตรวจสอบความยาวรหัสผ่าน (>= 8: Pass, < 8: Too Short)
    "Examination_3.py": [
        (["password123"], "Pass"),
        (["12345678"], "Pass"),
        (["abc"], "Too Short"),
        (["1234567"], "Too Short")
    ],
    # ข้อ 4: สัญญาณไฟจราจร (red: Stop, yellow: Slow, green: Go, อื่นๆ: Invalid)
    "Examination_4.py": [
        (["red"], "Stop"),
        (["yellow"], "Slow"),
        (["green"], "Go"),
        (["blue"], "Invalid")
    ],
    # ข้อ 5: คำนวณค่าไฟฟ้าตามหน่วย (<=50: หน่วยละ 3 บ., <=100: หน่วยละ 4 บ., >100: หน่วยละ 5 บ.)
    "Examination_5.py": [
        (["30"], "90"),
        (["50"], "150"),
        (["80"], "320"),
        (["120"], "600")
    ]
}

def find_file(base_name):
    """ค้นหาไฟล์รองรับทั้งชื่อที่มีและไม่มี .py"""
    if os.path.exists(base_name):
        return base_name
    elif os.path.exists(f"{base_name}.py"):
        return f"{base_name}.py"
    elif os.path.exists(base_name.replace(".py", "")):
        return base_name.replace(".py", "")
    return None

def run_test(file_path, inputs):
    """รันไฟล์และดึงค่า Output"""
    try:
        input_data = "\n".join(inputs)
        process = subprocess.run(
            [sys.executable, file_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=3,
            encoding='utf-8',
            errors='ignore'
        )
        return process.stdout.strip()
    except Exception:
        return None

def compare_outputs(actual, expected):
    """เปรียบเทียบผลลัพธ์ รองรับทั้งข้อความหลายบรรทัดและตัวเลข"""
    if actual is None:
        return False
    
    # ลบขอบช่องว่างและแปลงเป็นบรรทัดมาตรฐาน
    actual_lines = [line.strip() for line in actual.strip().splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected.strip().splitlines() if line.strip()]
    
    if actual_lines == expected_lines:
        return True
    
    actual_clean = " ".join(actual_lines)
    expected_clean = " ".join(expected_lines)
    
    if actual_clean.lower() == expected_clean.lower():
        return True
    
    try:
        return abs(float(actual_clean) - float(expected_clean)) < 1e-5
    except ValueError:
        return False

def main():
    total_score = 0
    max_total_score = 20
    summary_rows = []

    for exam_name, test_cases in EXAM_TEST_CASES.items():
        file_path = find_file(exam_name)
        passed_cases = 0
        total_cases = len(test_cases)
        
        if file_path:
            for inputs, expected in test_cases:
                output = run_test(file_path, inputs)
                if compare_outputs(output, expected):
                    passed_cases += 1
        
        # คำนวณคะแนนยืดหยุ่น: ผ่าน 1 เคส = 1 คะแนน
        score_for_exam = passed_cases 
        total_score += score_for_exam
        
        if passed_cases == total_cases:
            status_icon = "✅ ผ่านครบ"
        elif passed_cases > 0:
            status_icon = "🟡 ผ่านบางส่วน"
        else:
            status_icon = "❌ ไม่ผ่าน"

        summary_rows.append(
            f"| `{exam_name}` | {status_icon} | {passed_cases}/{total_cases} เคส | **{score_for_exam} / 4** |"
        )

    markdown_summary = f"""# 📊 สรุปผลการสอบวิชาเขียนโปรแกรม (Set 10)

| ข้อสอบ | สถานะการตรวจ | ผ่าน Test Cases | คะแนนที่ได้ |
| :--- | :---: | :---: | :---: |
{chr(10).join(summary_rows)}

---

### 🎯 **คะแนนรวมทั้งหมด: {total_score} / {max_total_score} คะแนน**
"""

    print(markdown_summary)

    summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
    if summary_file:
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(markdown_summary)

if __name__ == "__main__":
    main()
