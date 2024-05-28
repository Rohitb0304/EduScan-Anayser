# import fitz

# def convert_pdf_to_jpg(pdf_path, output_path):
#     """
#     Converts a PDF file to a JPG image with the best quality.

#     Args:
#         pdf_path: Path to the PDF file.
#         output_path: Path to save the JPG image.
#     """
#     doc = fitz.open(pdf_path)  # Open the PDF document

#     # Get the first page (modify the index for other pages)
#     page = doc.load_page(0)

#     # Get the default resolution of the page
#     default_resolution = 300  # Set your desired default resolution
#     zoom_x = default_resolution / 72.0
#     zoom_y = default_resolution / 72.0

#     # Render the page to a pixmap
#     pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom_x, zoom_y))

#     # Save the pixmap as a JPG image
#     pixmap.save(output_path)

#     print(f"PDF converted to JPG with best quality and saved to: {output_path}")

# # Example usage
# pdf_path = "/Users/rohitrajratnabansode/Downloads/Linux Certificates/Abhijeet Jagtap GFG MITA Linux.pdf"
# output_path = "output_image.jpg"
# convert_pdf_to_jpg(pdf_path, output_path)








import os
import fitz

def convert_pdf_to_jpg(pdf_path, output_folder):
    """
    Converts a PDF file to a JPG image with the best quality.

    Args:
        pdf_path: Path to the PDF file.
        output_folder: Path to the folder to save the JPG images.
    """
    # Open the PDF document
    doc = fitz.open(pdf_path)  

    # Iterate over each page in the PDF
    for i, page in enumerate(doc):
        # Get the default resolution of the page
        default_resolution = 300  # Set your desired default resolution
        zoom_x = default_resolution / 72.0
        zoom_y = default_resolution / 72.0

        # Render the page to a pixmap
        pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom_x, zoom_y))

        # Create output file path
        output_file = os.path.join(output_folder, f"{os.path.basename(pdf_path)[:-4]}_page_{i+1}.jpg")

        # Save the pixmap as a JPG image
        pixmap.save(output_file)
        print(f"Page {i+1} of PDF converted to JPG and saved to: {output_file}")

def convert_all_pdfs_to_jpg(input_folder, output_folder):
    """
    Converts all PDF files in a folder to JPG images.

    Args:
        input_folder: Path to the folder containing PDF files.
        output_folder: Path to the folder to save the JPG images.
    """
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            convert_pdf_to_jpg(pdf_path, output_folder)

# Example usage
input_folder = "BATU/"  # Change this to your input folder path
output_folder = "BATU/"  # Change this to your output folder path
convert_all_pdfs_to_jpg(input_folder, output_folder)