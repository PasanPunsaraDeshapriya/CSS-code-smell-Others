import pandas as pd

# === Load the feature dataset ===
df = pd.read_csv("css_features_all.csv")

# === Apply heuristics to assign labels ===
df['label'] = (
    (df['duplicate_selectors'] > 5) |
    (df['deep_nesting'] > 2) |
    (df['num_important'] > 3) |
    (df['inline_styles'] > 1) |
    (df['overqualified_selectors'] > 0) |
    (df['excessive_specificity'] > 2)
).astype(int)  # 1 = smelly, 0 = clean

# === Show label summary ===
print("\n🧼 Label distribution:")
print(df['label'].value_counts().rename({0: "Clean", 1: "Smelly"}))

# === Save the labeled dataset ===
df.to_csv("css_features_labeled.csv", index=False)
print(f"\n✅ Saved labeled dataset to css_features_labeled.csv")
