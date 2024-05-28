import re

def extract_course_info(text):
    # Define a regular expression pattern to match the course code and course name
    course_pattern = r'([A-Z]{3}\d{3})\s*\|?\s*(.+)'

    # Find all matches of the course pattern in the text
    matches = re.findall(course_pattern, text)

    # Extracted course information
    course_info = {}
    for match in matches:
        course_code, course_name = match
        course_info[course_code.strip()] = course_name.strip()

    return course_info

text = """
BSC204 ‘| Linear Algebra and Transform
CSE201 Data Structures
CSE202 | Discrete Mathematics & Graph Theory
CSE203 Digital Electronics & Microprocessor
~ CSE204 | Computer Organization and Architecture
CSE221 Lab-I: Data Structures
CSE222 Lab-II: Data Structures and Advanced Python Programming
CSE223 | Lab-II: Web Programming
CSE224 | Lab-IV: Digital Electronics and Microprocessor
CSE225 | Lab-V: Data Analytics
- HSM804___| Constitution of India
"""

# Extract course information
course_info = extract_course_info(text)

# Print course information
for course_code, course_name in course_info.items():
    print("Course Code:", course_code)
    print("Course Name:", course_name)
    print()
