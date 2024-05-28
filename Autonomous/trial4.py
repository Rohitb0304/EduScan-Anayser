import pytesseract
from PIL import Image
import fitz  # PyMuPDF for handling PDFs

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_file:
        for page_num in range(len(pdf_file)):
            page = pdf_file.load_page(page_num)
            text += page.get_text()
    return text

def extract_text_from_image(image_path):
    with Image.open(image_path) as img:
        text = pytesseract.image_to_string(img)
    return text

def print_formatted_text(text):
    print(text)

# Example usage
file_path = "Autonomous/Siyal-Marksheet.pdf"
if file_path.endswith(".pdf"):
    extracted_text = extract_text_from_pdf(file_path)
elif file_path.endswith((".jpg", ".jpeg", ".png")):
    extracted_text = extract_text_from_image(file_path)
else:
    extracted_text = "Unsupported file format."

print_formatted_text(extracted_text)