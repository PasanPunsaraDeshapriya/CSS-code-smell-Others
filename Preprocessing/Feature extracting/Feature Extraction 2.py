import os
import re
import csv

def extract_features(css_code):
    """
    Extract features from a single CSS file.
    """
    try:
        nesting_depth = css_code.count('{') - css_code.count('}')
        num_ids = css_code.count('#')
        num_classes = css_code.count('.')
        num_important = css_code.count('!important')
        selectors = re.findall(r'([^\{\}]+)\s*\{', css_code)
        duplicate_selectors = len(selectors) - len(set(selectors))
        return {
            'nesting_depth': nesting_depth,
            'num_ids': num_ids,
            'num_classes': num_classes,
            'num_important': num_important,
            'duplicate_selectors': duplicate_selectors
        }
    except Exception as e:
        print(f"Error processing CSS code: {e}")
        return {
            'nesting_depth': 0,
            'num_ids': 0,
            'num_classes': 0,
            'num_important': 0,
            'duplicate_selectors': 0
        }

def process_file(file_path, file_name):
    """
    Process a single CSS file to extract features.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            css_code = file.read()
        features = extract_features(css_code)
        features['file_name'] = file_name
        return features
    except Exception as e:
        print(f"Error reading file {file_name}: {e}")
        return None

def extract_features_sequentially(input_folder, output_csv):
    """
    Extract features from CSS files sequentially.
    """
    files = [
        (os.path.join(input_folder, file_name), file_name)
        for file_name in os.listdir(input_folder)
        if file_name.endswith(".css")
    ]

    total_files = len(files)
    processed_files = 0

    # Ensure the CSV is ready
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['file_name', 'nesting_depth', 'num_ids', 'num_classes', 'num_important', 'duplicate_selectors']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    for file_path, file_name in files:
        features = process_file(file_path, file_name)
        if features is not None:
            with open(output_csv, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(features)

        processed_files += 1
        print(f"Processed: {file_name}")
        print(f"Processed {processed_files}/{total_files} files ({(processed_files / total_files) * 100:.2f}%).")

    print(f"Feature extraction completed. Data saved to {output_csv}")

# Example usage
input_folder = r"D:\IIT 4th year\FYP\Preprocessing\Cleaning\CSS codes clean"
output_csv = r"D:\IIT 4th year\FYP\Preprocessing\Feature extracting\features.csv"

# Process files sequentially
extract_features_sequentially(input_folder, output_csv)
