import os
import re
import csv

def extract_features(css_code):
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

def extract_features_from_folder(input_folder, output_csv):
    features_list = []
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".css"):
            file_path = os.path.join(input_folder, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    css_code = file.read()
                features = extract_features(css_code)
                features['file_name'] = file_name
                features_list.append(features)
                print(f"Processed: {file_name}")
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")

    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['file_name', 'nesting_depth', 'num_ids', 'num_classes', 'num_important', 'duplicate_selectors']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(features_list)
        print(f"Feature extraction completed. Data saved to {output_csv}")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

# Paths
input_folder = r"D:\IIT 4th year\FYP\Preprocessing\Cleaning\CSS codes clean"
output_csv = r"D:\IIT 4th year\FYP\Preprocessing\Feature extracting\features.csv"
extract_features_from_folder(input_folder, output_csv)
