import os
import re

def normalize_css(css_code):
    """
    Normalize CSS content:
    - Convert to lowercase
    - Remove comments
    - Remove extra whitespace
    - Remove unnecessary semicolons
    - Format braces properly
    """
    css_code = css_code.lower()  # Convert to lowercase
    css_code = re.sub(r'/\*.*?\*/', '', css_code, flags=re.DOTALL)  # Remove comments
    css_code = re.sub(r'\s+', ' ', css_code).strip()  # Remove extra spaces and newlines
    css_code = re.sub(r';\s*}', '}', css_code)  # Remove semicolon before closing brace
    css_code = re.sub(r'\s*{\s*', '{', css_code)  # Remove spaces before/after '{'
    css_code = re.sub(r'\s*}\s*', '}', css_code)  # Remove spaces before/after '}'
    return css_code

def read_file_with_encoding(file_path):
    """
    Read a file with multiple encodings in case of UnicodeDecodeError.
    Tries UTF-8, ISO-8859-1, and Windows-1252.
    """
    encodings = ["utf-8", "ISO-8859-1", "Windows-1252"]
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()  # Successfully read the file
        except UnicodeDecodeError:
            print(f"⚠️ Warning: Could not decode {file_path} using {encoding}. Trying next encoding.")

    print(f"❌ Error: Could not read {file_path} with any encoding. Skipping file.")
    return None  # Return None if all encoding attempts fail

def normalize_all_css_files(input_folder, output_folder):
    """
    Normalize all CSS files in the input folder and save them to the output folder.
    """
    if not os.path.exists(input_folder):
        print(f"❌ Error: Input folder '{input_folder}' does not exist. Please check the path.")
        return
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create output folder if it doesn't exist

    # Process each file
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".css"):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name)

            # Read the file with proper encoding
            css_code = read_file_with_encoding(input_file_path)
            if css_code is None:
                continue  # Skip files that could not be read

            # Normalize the CSS content
            normalized_css = normalize_css(css_code)

            # Write the normalized CSS to the output folder
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(normalized_css)

            print(f"✅ Successfully normalized: {file_name}")

# Ensure paths are correctly formatted
input_folder = "D:\IIT 4th year\FYP\Creation\Preprocessing\Cleaning\All CSS codes unclean"
output_folder = "D:\IIT 4th year\FYP\Creation\Preprocessing\Cleaning\All CSS codes clean"
# Run the normalization process
normalize_all_css_files(input_folder, output_folder)
