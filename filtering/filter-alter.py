# import json

# # Read the original file
# with open('train_v2_fixed.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # Filter objects that have the "alter" key
# filtered_data = [obj for obj in data if 'alter' in obj and obj['alter']]

# # Take only the first 4000
# filtered_data = filtered_data[:4000]

# print(f"Total objects with 'alter' key: {len([obj for obj in data if 'alter' in obj and obj['alter']])}")
# print(f"Saving first {len(filtered_data)} objects")

# # Save to new file
# with open('train_v2_fixed_4000.json', 'w', encoding='utf-8') as f:
#     json.dump(filtered_data, f, ensure_ascii=False, indent=2)

# print("Done! Saved to train_v2_fixed_4000.json")

import json

# Read the original file
with open('train_v2_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Filter objects that have the "alter" key
filtered_data = [obj for obj in data if 'alter' in obj and obj['alter']]

print(f"Total objects with 'alter' key: {len(filtered_data)}")

# Save to new file
with open('train_v2_fixed_alter.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

print("Done! Saved to train_v2_fixed_alter.json")