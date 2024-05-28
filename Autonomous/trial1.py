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
        return "", "", "", ""

    roll_number_pattern = r'Seat No\s*:\s*(\d+)'
    name_pattern = r'Name\s*:\s*([A-Za-z\s]+)'
    program_pattern = r'Program Name\s*:\s*(.+)'
    exam_pattern = r'Examination\s*:\s*(.+)'

    roll_number = re.search(roll_number_pattern, text)
    name = re.search(name_pattern, text)
    program_name = re.search(program_pattern, text)
    exam_name = re.search(exam_pattern, text)

    if roll_number:
        roll_number = roll_number.group(1).strip()
    if name:
        name = name.group(1).strip()
    if program_name:
        program_name = program_name.group(1).strip()
    if exam_name:
        exam_name = exam_name.group(1).strip()

    return roll_number, name, program_name, exam_name

def save_to_csv(data, filename='Autonomous/output-result/result1.csv'):
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['Seat No', 'Name', 'Program Name', 'Examination']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow(data)

image_path = 'Autonomous/m2.jpg'
extracted_text = extract_text_from_image(image_path)

print("Extracted Text:")
print(extracted_text)

if extracted_text:
    roll_number, name, program_name, exam_name = process_marksheet(extracted_text)

    print("Processed Information:")
    print("Seat No:", roll_number)
    print("Name:", name)
    print("Program Name:", program_name)
    print("Examination:", exam_name)

    data = {'Seat No': roll_number, 'Name': name, 'Program Name': program_name, 'Examination': exam_name}
    save_to_csv(data)
else:
    print("Error: Text extraction failed.")
