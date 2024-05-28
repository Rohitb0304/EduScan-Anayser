import csv
import pytesseract
from PIL import Image
import re
import os

def extract_text_from_image(image_path):
    try:
        _, file_extension = os.path.splitext(image_path)
        if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
            image = Image.open(image_path)
        else:
            raise ValueError("Unsupported image format")
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        print("Error during text extraction:", e)
        return None

def process_marksheet(text):
    if text is None:
        print("Error: Text extraction failed.")
        return "", "", "", "", "", "", "", "", ""

    roll_number_pattern = r'Seat No\s*:\s*(\d+)'
    name_pattern = r'Name\s*:\s*([A-Za-z\s]+)'
    program_pattern = r'Program Name\s*:\s*(.+)'
    exam_pattern = r'Examination\s*:\s*(.+)'
    sgpa_pattern = r'SGPA:\s*(\d+\.\d+)'
    cgpa_pattern = r'CGPA:\s*(\d+\.\d+)'
    total_credits_pattern = r'Total Credits:\s*(\d+)'
    total_egp_pattern = r'Total EGP:\s*(\d+)'
    status_pattern = r'Status\s*:\s*(\w+)'
    linear_algebra = r'Linear Algebra and Transform\s:([0-9].+)'

    roll_number = re.search(roll_number_pattern, text)
    name = re.search(name_pattern, text)
    program_name = re.search(program_pattern, text)
    exam_name = re.search(exam_pattern, text)
    sgpa_match = re.search(sgpa_pattern, text)
    cgpa_match = re.search(cgpa_pattern, text)
    total_credits_match = re.search(total_credits_pattern, text)
    total_egp_match = re.search(total_egp_pattern, text)
    status_match = re.search(status_pattern, text)
    linear_algebra = re.search(linear_algebra, text)

    if roll_number:
        roll_number = roll_number.group(1).strip()
    if name:
        name = name.group(1).strip()
    if program_name:
        program_name = program_name.group(1).strip()
    if exam_name:
        exam_name = exam_name.group(1).strip()
    sgpa = sgpa_match.group(1).strip() if sgpa_match else "NA"
    cgpa = cgpa_match.group(1).strip() if cgpa_match else "NA"
    total_credits = total_credits_match.group(1).strip() if total_credits_match else "NA"
    total_egp = total_egp_match.group(1).strip() if total_egp_match else "NA"
    status = status_match.group(1).strip() if status_match else "NA"
    linear_algebra = linear_algebra.group(1).strip() if linear_algebra else "NA"

    return roll_number, name, program_name, exam_name, linear_algebra, sgpa, cgpa, total_credits, total_egp, status

def save_to_csv(data,  sgpa, cgpa, total_credits, linear_algebra,  total_egp, status, course_info, filename='Autonomous/output-result/course-try.csv'):
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['Seat No', 'Name', 'Program Name', 'Examination', 'SGPA', 'CGPA', 'Total Credits', 'Linear Algebra and Transform', 'Total EGP', 'Status'] + list(course_info.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({**data, 'SGPA': sgpa, 'CGPA': cgpa, 'Total Credits': total_credits, 'Total EGP': total_egp, 'Status': status, **course_info})

image_path = 'Autonomous/m2.jpg'
extracted_text = extract_text_from_image(image_path)

print("Extracted Text:")
print(extracted_text)

if extracted_text:
    roll_number, name, program_name, exam_name, sgpa, cgpa, total_credits, linear_algebra, total_egp, status = process_marksheet(extracted_text)

    print("Processed Information:")
    print("Seat No:", roll_number)
    print("Name:", name)
    print("Program Name:", program_name)
    print("Examination:", exam_name)
    print("SGPA:", sgpa)
    print("CGPA:", cgpa)
    print("Total Credits:", total_credits)
    print("Linear Algebra and Transform: ", linear_algebra)
    print("Total EGP:", total_egp)
    print("Status:", status)

    data = {'Seat No': roll_number, 'Name': name, 'Program Name': program_name, 'Examination': exam_name}
    save_to_csv(data, sgpa, cgpa, total_credits,linear_algebra , total_egp, status, {})
else:
    print("Error: Text extraction failed.")