# import csv
# import pytesseract
# from PIL import Image
# import re
# import os

# class MarksheetI:
#     def __init__(self, image_path):
#         self.image_path = image_path

# def extract_prn_and_name(image_path):
#     try:
#         img = Image.open(image_path)
#         text = pytesseract.image_to_string(img)

#         # Define a regular expression pattern for PRN and Student's Name
#         prn_pattern = re.compile(r'PRN\s+2\s+(\d{13})')
#         name_pattern = re.compile(r"STUDENT'S NAME\s*:\s*(.+)")

#         # Extract PRN and Student's Name
#         prn_match = prn_pattern.search(text)
#         name_match = name_pattern.search(text)

#         prn = prn_match.group(1) if prn_match else ''
#         name = name_match.group(1) if name_match else ''

#         return {'PRN': prn, "STUDENT'S NAME": name}

#     except Exception as e:
#         print(f"Error: {e}")
#         return f"Error: {e}"

# def extract_subject_data(image_path):
#     try:
#         img = Image.open(image_path)
#         text = pytesseract.image_to_string(img)

#         # Remove unwanted text
#         text = re.sub(r'\bCONTROLLER OF EXAMINATIONS\b.*', '', text)

#         # Define a regular expression pattern for subject information
#         pattern = re.compile(r'(ENGINEERING MATHEMATICS(?:\s*-\s*\|)?|ENGINEERING CHEMISTRY|ENGINEERING MECHANICS|COMPUTER PROGRAMMING IN C|WORKSHOP PRACTICES|Basic Electrical and Electronics Engineering)\s+(\d+|[A-Za-z]{2})\s*([A-Za-z]{1,2})([A-Za-z]{1,2})')

#         subject_data = {}
#         matches = pattern.findall(text)

#         for match in matches:
#             subject_name, credits, grade1, grade2 = match
#             # Concatenate the two alphabet characters for the grade
#             grade = grade1 + grade2
#             # Normalize subject name for easier matching
#             subject_name = subject_name.strip().upper().replace('-', '').replace('|', '').strip()
#             subject_data[subject_name] = {'Credits': credits, 'Grade': grade}

#         # If the grade for Basic Electrical and Electronics Engineering is not found, set it to an empty string
#         if 'BASIC ELECTRICAL AND ELECTRONICS ENGINEERING' not in subject_data:
#             subject_data['BASIC ELECTRICAL AND ELECTRONICS ENGINEERING'] = {'Credits': '', 'Grade': ''}

#         return subject_data

#     except Exception as e:
#         print(f"Error: {e}")
#         return {}

# def locate_cgpa_sgpa(image_path, cgpa_coords, sgpa_coords):
#     try:
#         # Process the image using OCR to extract text
#         img = Image.open(image_path)

#         # Extract CGPA and SGPA using provided coordinates
#         cgpa_text = pytesseract.image_to_string(img.crop(cgpa_coords))
#         sgpa_text = pytesseract.image_to_string(img.crop(sgpa_coords))

#         # Extracted CGPA and SGPA
#         cgpa = cgpa_text.strip() if cgpa_text else None
#         sgpa = sgpa_text.strip() if sgpa_text else None

#         return {'CGPA': cgpa, 'SGPA': sgpa}

#     except Exception as e:
#         print(f"Error locating CGPA and SGPA: {e}")
#         return {'CGPA': None, 'SGPA': None}

# def save_data_to_csv_with_default_headers(output_path, prn_and_name, subject_data, cgpa_sgpa):
#     # Define default headers
#     default_headers = ['PRN', "STUDENT'S NAME", "ENGINEERING MATHEMATICS", 'ENGINEERING CHEMISTRY', 'ENGINEERING MECHANICS', 'COMPUTER PROGRAMMING IN C', 'WORKSHOP PRACTICES', 'Basic Electrical and Electronics Engineering', 'SGPA', 'CGPA']

#     # Check if the file already exists
#     file_exists = os.path.exists(output_path)

#     with open(output_path, 'a', newline='') as csv_file:
#         writer = csv.writer(csv_file)

#         # Write header only if the file doesn't exist yet
#         if not file_exists:
#             print("Headers in CSV file:", default_headers)  # Print headers
#             writer.writerow(default_headers)

#         # Write PRN and Student's Name
#         prn_row = [prn_and_name.get(header, '') for header in default_headers[:2]]

#         # Write subject grades
#         subjects_row = [subject_data.get(header, {}).get('Grade', '') for header in default_headers[2:8]]

#         # Write SGPA and CGPA
#         sgpa_cgpa_row = [cgpa_sgpa.get('SGPA', ''), cgpa_sgpa.get('CGPA', '')]

#         writer.writerow(prn_row + subjects_row + sgpa_cgpa_row)


# # Specify the file path to the image
# image_file_path = 'BATU/marksheet.png'

# # Extract PRN and Student's Name
# prn_and_name = extract_prn_and_name(image_file_path)

# # Extract subject data using regular expressions
# subject_data = extract_subject_data(image_file_path)

# # Define coordinates for CGPA and SGPA
# cgpa_coords = (1173, 1594, 1243, 1620)
# sgpa_coords = (549, 1595, 618, 1624)

# # Locate CGPA and SGPA
# cgpa_sgpa = locate_cgpa_sgpa(image_file_path, cgpa_coords, sgpa_coords)

# # Specify the output path for the CSV file
# output_path = 'BATU/output/data2.csv'

# # Save data to CSV with default headers
# save_data_to_csv_with_default_headers(output_path, prn_and_name, subject_data, cgpa_sgpa)

# # Print extracted data for debugging
# print("PRN and Name:", prn_and_name)
# print("Subjects Data:", subject_data)
# print("CGPA and SGPA:", cgpa_sgpa)




import csv
import pytesseract
from PIL import Image
import re
import os
import tempfile
from pdf2image import convert_from_path

class MarksheetI:
    def __init__(self, image_path):
        self.image_path = image_path

def extract_prn_and_name(image):
    try:
        text = pytesseract.image_to_string(image)

        # Define a regular expression pattern for PRN and Student's Name
        prn_pattern = re.compile(r'PRN\s+2\s+(\d{13})')
        name_pattern = re.compile(r"STUDENT'S NAME\s*:\s*(.+)")

        # Extract PRN and Student's Name
        prn_match = prn_pattern.search(text)
        name_match = name_pattern.search(text)

        prn = prn_match.group(1) if prn_match else ''
        name = name_match.group(1) if name_match else ''

        return {'PRN': prn, "STUDENT'S NAME": name}

    except Exception as e:
        print(f"Error: {e}")
        return {}

def extract_subject_data(image):
    try:
        text = pytesseract.image_to_string(image)

        # Remove unwanted text
        text = re.sub(r'\bCONTROLLER OF EXAMINATIONS\b.*', '', text)

        # Define a regular expression pattern for subject information
        pattern = re.compile(r'(ENGINEERING MATHEMATICS(?:\s*-\s*\|)?|ENGINEERING CHEMISTRY|ENGINEERING MECHANICS|COMPUTER PROGRAMMING IN C|WORKSHOP PRACTICES|Basic Electrical and Electronics Engineering)\s+(\d+|[A-Za-z]{2})\s*([A-Za-z]{1,2})([A-Za-z]{1,2})')

        subject_data = {}
        matches = pattern.findall(text)

        for match in matches:
            subject_name, credits, grade1, grade2 = match
            # Concatenate the two alphabet characters for the grade
            grade = grade1 + grade2
            # Normalize subject name for easier matching
            subject_name = subject_name.strip().upper().replace('-', '').replace('|', '').strip()
            subject_data[subject_name] = {'Credits': credits, 'Grade': grade}

        # If the grade for Basic Electrical and Electronics Engineering is not found, set it to an empty string
        if 'BASIC ELECTRICAL AND ELECTRONICS ENGINEERING' not in subject_data:
            subject_data['BASIC ELECTRICAL AND ELECTRONICS ENGINEERING'] = {'Credits': '', 'Grade': ''}

        return subject_data

    except Exception as e:
        print(f"Error: {e}")
        return {}

def locate_cgpa_sgpa(image, cgpa_coords, sgpa_coords):
    try:
        # Extract CGPA and SGPA using provided coordinates
        cgpa_text = pytesseract.image_to_string(image.crop(cgpa_coords))
        sgpa_text = pytesseract.image_to_string(image.crop(sgpa_coords))

        # Extracted CGPA and SGPA
        cgpa = cgpa_text.strip() if cgpa_text else None
        sgpa = sgpa_text.strip() if sgpa_text else None

        return {'CGPA': cgpa, 'SGPA': sgpa}

    except Exception as e:
        print(f"Error locating CGPA and SGPA: {e}")
        return {'CGPA': None, 'SGPA': None}

def save_data_to_csv_with_default_headers(output_path, prn_and_name, subject_data, cgpa_sgpa):
    # Define default headers
    default_headers = ['PRN', "STUDENT'S NAME", "ENGINEERING MATHEMATICS", 'ENGINEERING CHEMISTRY', 'ENGINEERING MECHANICS', 'COMPUTER PROGRAMMING IN C', 'WORKSHOP PRACTICES', 'Basic Electrical and Electronics Engineering', 'SGPA', 'CGPA']

    # Check if the file already exists
    file_exists = os.path.exists(output_path)

    with open(output_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write header only if the file doesn't exist yet
        if not file_exists:
            print("Headers in CSV file:", default_headers)  # Print headers
            writer.writerow(default_headers)

        # Write PRN and Student's Name
        prn_row = [prn_and_name.get(header, '') for header in default_headers[:2]]

        # Write subject grades
        subjects_row = [subject_data.get(header, {}).get('Grade', '') for header in default_headers[2:8]]

        # Write SGPA and CGPA
        sgpa_cgpa_row = [cgpa_sgpa.get('SGPA', ''), cgpa_sgpa.get('CGPA', '')]

        writer.writerow(prn_row + subjects_row + sgpa_cgpa_row)


def process_document(document_path, cgpa_coords, sgpa_coords, output_path):
    _, file_extension = os.path.splitext(document_path)
    if file_extension.lower() in ['.jpg', '.jpeg', '.png']:
        img = Image.open(document_path)
        prn_and_name = extract_prn_and_name(img)
        subject_data = extract_subject_data(img)
        cgpa_sgpa = locate_cgpa_sgpa(img, cgpa_coords, sgpa_coords)
        print("PRN and Name:", prn_and_name)
        print("Subject Data:", subject_data)
        print("CGPA and SGPA:", cgpa_sgpa)
        save_data_to_csv_with_default_headers(output_path, prn_and_name, subject_data, cgpa_sgpa)
    elif file_extension.lower() == '.pdf':
        with tempfile.TemporaryDirectory() as temp_dir:
            images = convert_from_path(document_path, output_folder=temp_dir)
            for i, image in enumerate(images):
                prn_and_name = extract_prn_and_name(image)
                subject_data = extract_subject_data(image)
                cgpa_sgpa = locate_cgpa_sgpa(image, cgpa_coords, sgpa_coords)
                print(f"Page {i+1}:")
                print("PRN and Name:", prn_and_name)
                print("Subject Data:", subject_data)
                print("CGPA and SGPA:", cgpa_sgpa)
                save_data_to_csv_with_default_headers(output_path, prn_and_name, subject_data, cgpa_sgpa)


# Specify the file path to the document
# document_path = 'BATU/marksheet.png'
document_path = 'BATU/Sanskar markesheet 2_page_1.jpg'
# Define coordinates for CGPA and SGPA
cgpa_coords = (1173, 1594, 1243, 1620)
sgpa_coords = (549, 1595, 618, 1624)

# Specify the output path for the CSV file
output_path = 'BATU/output/OUTPUT.csv'

# Process document and save data to CSV
process_document(document_path, cgpa_coords, sgpa_coords, output_path)