import os
import cssbeautifier

# ✅ Define Input and Output Folder
INPUT_FOLDER = r"D:\IIT 4th year\FYP\Creation\Preprocessing\Cleaning\CSS codes clean"  # Update this path
OUTPUT_FOLDER = r"D:\IIT 4th year\FYP\Creation\Preprocessing\Cleaning\CSS code formatted"  # Save formatted files in a new folder

# ✅ Ensure the output directory exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# ✅ Function to format a single CSS file
def format_css_file(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        css_code = file.read()

    # Use cssbeautifier to format the CSS code
    formatted_css = cssbeautifier.beautify(css_code, {
        "indent_size": 4,  # Adjust indentation (4 spaces)
        "selector_separator_newline": True,  # Ensure new lines between selectors
        "end_with_newline": True  # End file with a newline
    })

    # Save the formatted CSS
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(formatted_css)

    print(f"✅ Formatted: {os.path.basename(file_path)}")

# ✅ Process all CSS files in the input folder
def format_all_css_files(input_folder, output_folder):
    files = [f for f in os.listdir(input_folder) if f.endswith(".css")]
    
    if not files:
        print("❌ No CSS files found in the folder.")
        return

    total_files = len(files)
    formatted_files = 0

    for file_name in files:
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        format_css_file(input_path, output_path)
        formatted_files += 1

        print(f"Processed {formatted_files}/{total_files} files ({(formatted_files / total_files) * 100:.2f}%).")

    print(f"\n🎉 All CSS files formatted successfully! Saved to: {output_folder}")

# ✅ Run the script
format_all_css_files(INPUT_FOLDER, OUTPUT_FOLDER)
