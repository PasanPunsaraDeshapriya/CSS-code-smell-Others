import os
import re

def normalize_css(css_code):
    """
    Normalize a single CSS file's content.
    - Lowercase all text.
    - Remove comments.
    - Remove extra whitespace.
    - Remove unnecessary semicolons or braces.
    """
    # Lowercase the content
    css_code = css_code.lower()
    
    # Remove CSS comments
    css_code = re.sub(r'/\*.*?\*/', '', css_code, flags=re.DOTALL)
    
    # Remove extra whitespace and line breaks
    css_code = re.sub(r'\s+', ' ', css_code).strip()
    
    # Remove unnecessary semicolons
    css_code = re.sub(r';\s*}', '}', css_code)
    
    # Remove redundant braces (optional step)
    css_code = re.sub(r'\s*{\s*', '{', css_code)
    css_code = re.sub(r'\s*}\s*', '}', css_code)
    
    return css_code

def normalize_all_css_files(input_folder, output_folder):
    """
    Normalize all CSS files in the input folder and save them to the output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".css"):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name)
            
            with open(input_file_path, 'r', encoding='utf-8') as file:
                css_code = file.read()
            
            # Normalize the CSS file
            normalized_css = normalize_css(css_code)
            
            # Save the normalized CSS to the output folder
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(normalized_css)
            
            print(f"Normalized: {file_name}")

# Example usage
input_folder = "D:\IIT 4th year\FYP\Cleaning\CSS codes unclean"
output_folder = "D:\IIT 4th year\FYP\Cleaning\CSS codes clean"
normalize_all_css_files(input_folder, output_folder)
