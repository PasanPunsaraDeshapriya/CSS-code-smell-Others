import os
import re
import csv

# ✅ Define Input Folder (Ensure This Path Exists)
INPUT_FOLDER = r"D:\IIT 4th year\FYP\Preprocessing\Cleaning\CSS codes clean"
OUTPUT_CSV = r"D:\IIT 4th year\FYP\Preprocessing\Cleaning\css_features.csv"

# ✅ Ensure the directory exists before proceeding
if not os.path.exists(INPUT_FOLDER):
    raise FileNotFoundError(f"Error: The directory '{INPUT_FOLDER}' does not exist. Please check the path.")

# Feature extraction function
def extract_features_from_css(css_code):
    """
    Extract 20+ features from a single CSS file.
    """
    nesting_depth = css_code.count('{') - css_code.count('}')
    num_ids = css_code.count('#')
    num_classes = css_code.count('.')
    num_important = css_code.count('!important')
    duplicate_selectors = len(re.findall(r'([^\{\}]+)\s*\{', css_code)) - len(set(re.findall(r'([^\{\}]+)\s*\{', css_code)))

    total_rules = css_code.count('}')
    deep_nesting = max([line.count('{') for line in css_code.split('\n') if '{' in line] + [0])
    long_selectors = sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if len(selector) > 50)
    overqualified_selectors = sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if 'html' in selector or 'body' in selector)
    browser_specific_properties = sum(1 for prop in re.findall(r'-(moz|webkit|ms|o)-', css_code))

    total_properties = css_code.count(';')
    avg_properties_per_rule = total_properties / (total_rules + 1)
    inline_styles = css_code.count('style=')
    unused_selectors = sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if len(selector.split()) > 3)
    universal_selectors = css_code.count('*')
    excessive_specificity = sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if selector.count(' ') > 3)
    vendor_prefixes = sum(1 for _ in re.findall(r'-(webkit|moz|ms|o)-', css_code))
    animation_usage = css_code.count('@keyframes')
    excessive_zindex = sum(1 for prop in re.findall(r'z-index\s*:\s*(\d+)', css_code) if int(prop) > 10)
    unused_media_queries = sum(1 for mq in re.findall(r'@media\s*\((.*?)\)', css_code) if 'print' in mq or 'speech' in mq)
    color_hex_usage = css_code.count('#')
    excessive_font_sizes = sum(1 for prop in re.findall(r'font-size\s*:\s*(\d+)', css_code) if int(prop) > 40)

    return {
        "nesting_depth": nesting_depth, "num_ids": num_ids, "num_classes": num_classes,
        "num_important": num_important, "duplicate_selectors": duplicate_selectors,
        "total_rules": total_rules, "deep_nesting": deep_nesting, "long_selectors": long_selectors,
        "overqualified_selectors": overqualified_selectors, "browser_specific_properties": browser_specific_properties,
        "total_properties": total_properties, "avg_properties_per_rule": avg_properties_per_rule,
        "inline_styles": inline_styles, "unused_selectors": unused_selectors,
        "universal_selectors": universal_selectors, "excessive_specificity": excessive_specificity,
        "vendor_prefixes": vendor_prefixes, "animation_usage": animation_usage,
        "excessive_zindex": excessive_zindex, "unused_media_queries": unused_media_queries,
        "color_hex_usage": color_hex_usage, "excessive_font_sizes": excessive_font_sizes
    }

# ✅ Process CSS files safely with path validation
def process_css_files(input_folder, output_csv):
    files = [(os.path.join(input_folder, file_name), file_name) for file_name in os.listdir(input_folder) if file_name.endswith(".css")]
    total_files = len(files)
    processed_files = 0

    if total_files == 0:
        raise FileNotFoundError("Error: No .css files found in the specified directory.")

    fieldnames = [
        "file_name", "nesting_depth", "num_ids", "num_classes", "num_important", "duplicate_selectors",
        "total_rules", "deep_nesting", "long_selectors", "overqualified_selectors", "browser_specific_properties",
        "total_properties", "avg_properties_per_rule", "inline_styles", "unused_selectors", "universal_selectors",
        "excessive_specificity", "vendor_prefixes", "animation_usage", "excessive_zindex", "unused_media_queries",
        "color_hex_usage", "excessive_font_sizes"
    ]

    # ✅ Create CSV file with headers before appending data
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for file_path, file_name in files:
        with open(file_path, 'r', encoding='utf-8') as file:
            css_code = file.read()
        
        features = extract_features_from_css(css_code)
        features["file_name"] = file_name  # Add filename to the feature dictionary

        # ✅ Append results to CSV safely
        with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(features)

        # ✅ Progress Logging
        processed_files += 1
        print(f"Processed: {file_name}")
        print(f"Processed {processed_files}/{total_files} files ({(processed_files / total_files) * 100:.2f}%).")

    print(f"✅ Feature extraction completed. Data saved to {output_csv}")

# ✅ Run the script
process_css_files(INPUT_FOLDER, OUTPUT_CSV)
