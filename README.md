Sure, here's the properly formatted `README.md` with all steps correctly inside the markdown view:

## `README.md`

```markdown
# Marksheet Text Extraction and Processing

This project extracts and processes text from marksheets using OCR (Optical Character Recognition) and stores the processed data into a CSV file.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

### Step 1: Install Python

Download and install the latest version of Python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/).

### Step 2: Install Tesseract OCR

- **Windows**: Download the Tesseract installer from [here](https://github.com/UB-Mannheim/tesseract/wiki). Run the installer and add Tesseract to your system path.
- **macOS**: Use Homebrew to install Tesseract:
  ```sh
  brew install tesseract
  
- **Linux**: Use the package manager to install Tesseract:
  ```sh
  sudo apt-get install tesseract-ocr
  

### Step 3: Set Up the Project

1. **Clone the Repository** (if applicable) or Download the project files.

2. **Navigate to the Project Directory**:
   ```sh
   cd <project-directory>
   

3. **Create a Virtual Environment** (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   

4. **Install Required Python Packages**:
   ```sh
   pip install -r requirements.txt
   

### Step 4: Run the Application

To run the application and extract text from a marksheet image:

1. Place the marksheet image in the `Autonomous` directory.

2. Modify the `image_path` variable in the script to point to your image file.

3. Run the script:
   ```sh
   python <script_name>.py
   ```

## Usage

The script processes the image, extracts relevant details, and saves them in a CSV file located in the `Autonomous/output-result/` directory. Ensure that you have the necessary permissions to read/write files in this directory.

## Notes

- Ensure that the marksheet image is in a supported format (`.jpg`, `.jpeg`, `.png`).
- Adjust the regular expressions in the `process_marksheet` function if the structure of the marksheet text changes.

## Troubleshooting

- **Tesseract Not Found**: Ensure Tesseract is installed and added to your system's PATH.
- **Missing Modules**: Ensure all required modules are installed by running `pip install -r requirements.txt`.
- **Permissions Issues**: Ensure you have read/write permissions for the directories where images and CSV files are located.

## Contributing

Feel free to submit issues or pull requests to improve this project.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
```

You can now copy and paste the entire content above into your `README.md` file, and all steps will be correctly formatted within the markdown view.
