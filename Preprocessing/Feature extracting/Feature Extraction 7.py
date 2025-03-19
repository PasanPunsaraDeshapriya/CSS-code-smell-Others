import os
import re
import csv

# ✅ Define Paths
INPUT_FOLDER = r"D:\IIT 4th year\FYP\Creation\Preprocessing\Cleaning\CSS code formatted"
OUTPUT_FOLDER = r"D:\IIT 4th year\FYP\Creation\Preprocessing\Feature extracting"  # Ensure this matches where you want to save
OUTPUT_CSV = os.path.join(OUTPUT_FOLDER, "css_features_2.csv")

# ✅ Set Batch Range (MANUALLY CHANGE THESE VALUES FOR EACH RUN)
start_index = 50   # Change this to process next batch (e.g., 50, 100, etc.)
end_index = 500    # Change this to process next batch (e.g., 100, 150, etc.)

# ✅ Ensure output directory exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# ✅ Ensure input folder exists
if not os.path.exists(INPUT_FOLDER):
    raise FileNotFoundError(f"❌ ERROR: The directory '{INPUT_FOLDER}' does not exist.")

# ✅ Feature Extraction Function
def extract_features_from_css(css_code):
    nesting_depth = css_code.count('{') - css_code.count('}')
    num_ids = css_code.count('#')
    num_classes = css_code.count('.')
    num_important = css_code.count('!important')
    duplicate_selectors = len(re.findall(r'([^\{\}]+)\s*\{', css_code)) - len(set(re.findall(r'([^\{\}]+)\s*\{', css_code)))
    total_rules = css_code.count('}')
    deep_nesting = max([line.count('{') for line in css_code.split('\n') if '{' in line] + [0])
    long_selectors = sum(1 for selector in re.findall(r'([^\{\}]+)\s*\{', css_code) if len(selector) > 50)
    overqualified_selectors = sum(1 for selector in re.split(r'\s*\{', css_code) if 'html' in selector or 'body' in selector)
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

# ✅ Process CSS Files in Manual Batch
def process_css_files(input_folder, output_csv, start_index, end_index):
    files = [(os.path.join(input_folder, file_name), file_name) for file_name in os.listdir(input_folder) if file_name.endswith(".css")]
    total_files = len(files)
    
    if start_index >= total_files:
        print(f"⚠️ No more files to process! The dataset has only {total_files} files.")
        return

    # Adjust the end_index if it exceeds total_files
    end_index = min(end_index, total_files)

    fieldnames = ["file_name"] + list(extract_features_from_css("").keys())

    # ✅ Create CSV file with headers only for the first batch
    if start_index == 0:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    processed_files = 0

    # Process only the files in the specified range
    for file_path, file_name in files[start_index:end_index]:
        with open(file_path, 'r', encoding='utf-8', errors="ignore") as file:
            css_code = file.read()
        print(f"🔍 Now Processing: {file_name}")
        features = extract_features_from_css(css_code)
        features["file_name"] = file_name

        with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(features)

        processed_files += 1
        print(f"Processed {start_index + processed_files}/{total_files} files ({((start_index + processed_files) / total_files) * 100:.2f}%).")
        print(f"✅ file {file_name}")


    print(f"\n🎉 Batch processing completed! Files {start_index} to {end_index} processed. Data saved to {OUTPUT_CSV}")

# ✅ Run Extraction for the Specified Batch
process_css_files(INPUT_FOLDER, OUTPUT_CSV, start_index, end_index)
