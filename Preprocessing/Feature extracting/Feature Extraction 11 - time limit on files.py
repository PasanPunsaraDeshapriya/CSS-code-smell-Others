import os
import re
import csv
import time
from tqdm import tqdm  # For progress bar

# Constants
TIMEOUT_DURATION = 60  # seconds

# Paths
INPUT_FOLDER = r"D:\Documents\IIT\FYP\CSS-code-smell-Others\Preprocessing\Cleaning\CSS code formatted - all"
OUTPUT_FOLDER = r"D:\Documents\IIT\FYP\CSS-code-smell-Others\Preprocessing\Feature extracting"
OUTPUT_CSV = os.path.join(OUTPUT_FOLDER, "css_features_all.csv")
SKIPPED_FILE_LOG = os.path.join(OUTPUT_FOLDER, "skipped_files.txt")

# Ensure the directory exists before proceeding
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

# Process CSS files safely with path validation
def process_css_files(input_folder, output_csv):
    files = [(os.path.join(input_folder, file_name), index + 1) for index, file_name in enumerate(os.listdir(input_folder)) if file_name.endswith(".css")]
    total_files = len(files)
    processed_files = 0

    if total_files == 0:
        raise FileNotFoundError("Error: No .css files found in the specified directory.")

    fieldnames = [
        "file_number", "nesting_depth", "num_ids", "num_classes", "num_important", "duplicate_selectors",
        "total_rules", "deep_nesting", "long_selectors", "overqualified_selectors", "browser_specific_properties",
        "total_properties", "avg_properties_per_rule", "inline_styles", "unused_selectors", "universal_selectors",
        "excessive_specificity", "vendor_prefixes", "animation_usage", "excessive_zindex", "unused_media_queries",
        "color_hex_usage", "excessive_font_sizes"
    ]

    # Create CSV file with headers before appending data
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    # Use tqdm to display a progress bar
    for file_path, file_number in tqdm(files, desc="Processing CSS files", unit="file"):
        start_time = time.time()

        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as file:
                css_code = file.read()

            # Check elapsed time after reading the file
            elapsed_time = time.time() - start_time
            if elapsed_time > TIMEOUT_DURATION:
                with open(SKIPPED_FILE_LOG, 'a', encoding='utf-8') as skip_log:
                    skip_log.write(f"{os.path.basename(file_path)}\n")
                print(f"⚠️ Skipped: File {file_number} ({os.path.basename(file_path)}) took {elapsed_time:.2f}s.")
                continue

            # Extract features
            features = extract_features_from_css(css_code)

            # Check elapsed time after feature extraction
            elapsed_time = time.time() - start_time
            if elapsed_time > TIMEOUT_DURATION:
                with open(SKIPPED_FILE_LOG, 'a', encoding='utf-8') as skip_log:
                    skip_log.write(f"{os.path.basename(file_path)}\n")
                print(f"⚠️ Skipped: File {file_number} ({os.path.basename(file_path)}) took {elapsed_time:.2f}s.")
                continue

            features["file_number"] = file_number

            # Append results to CSV safely
            with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(features)

            processed_files += 1

        except Exception as e:
            print(f"❌ Error processing file {file_number} ({os.path.basename(file_path)}): {e}")
            continue

    print(f"✅ Feature extraction completed. Data saved to {output_csv}")

# Run the script
process_css_files(INPUT_FOLDER, OUTPUT_CSV)