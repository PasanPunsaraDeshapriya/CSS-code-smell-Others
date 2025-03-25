import pandas as pd

# === Load the feature dataset ===
df = pd.read_csv("css_features_all_small.csv")
print("📋 Columns in dataset:", df.columns.tolist())

# === Helper function that only adds condition if column exists ===
conditions = []

def add_condition(col, condition_fn):
    if col in df.columns:
        condition = condition_fn(df[col])
        conditions.append(condition)
    else:
        print(f"⚠️ Skipped missing column: '{col}'")

# === Add all your heuristics ===
add_condition('total_rules', lambda x: x > 100)
add_condition('total_selectors', lambda x: x > 150)
add_condition('num_ids', lambda x: x > 2)
add_condition('num_classes', lambda x: x > 30)
add_condition('num_elements', lambda x: x > 40)
add_condition('max_selector_depth', lambda x: x > 4)
add_condition('avg_selector_depth', lambda x: x > 3)
add_condition('num_important', lambda x: x > 3)
add_condition('duplicate_properties', lambda x: x > 5)
add_condition('num_comments', lambda x: x < 1)
add_condition('num_media_queries', lambda x: x > 5)
add_condition('num_keyframes', lambda x: x > 3)
add_condition('max_properties_per_rule', lambda x: x > 10)
add_condition('avg_properties_per_rule', lambda x: x > 8)
add_condition('color_hardcoding_count', lambda x: x > 10)
add_condition('font_hardcoding_count', lambda x: x > 5)
add_condition('deeply_nested_rules', lambda x: x > 10)
add_condition('num_vendor_prefixes', lambda x: x > 5)
add_condition('inline_style_count', lambda x: x > 5)
add_condition('global_class_reuse', lambda x: x > 20)
add_condition('property_redundancy', lambda x: x > 2)
add_condition('zero_units', lambda x: x > 10)
add_condition('multiple_backgrounds', lambda x: x > 3)
add_condition('shorthand_overrides', lambda x: x > 3)
add_condition('selector_specificity_score', lambda x: x > 1000)

# === Assign label based on OR of all conditions ===
if conditions:
    df['label'] = pd.concat(conditions, axis=1).any(axis=1).astype(int)
else:
    print("❌ No valid features found. Defaulting to 'clean'.")
    df['label'] = 0

# === Show label summary ===
print("\n🧼 Label distribution:")
print(df['label'].value_counts().rename({0: "Clean", 1: "Smelly"}))

# === Save the labeled dataset ===
output_file = "css_features_small_labeled_heuristic.csv"
df.to_csv(output_file, index=False)
print(f"\n✅ Saved labeled dataset to {output_file}")
