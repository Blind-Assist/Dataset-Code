import json

input_file = "train/metadata.jsonl"
output_file = "train/metadata_fixed.jsonl"

with open(input_file, 'r', encoding='utf-8') as f_in, \
     open(output_file, 'w', encoding='utf-8') as f_out:
    
    for line in f_in:
        entry = json.loads(line)
        
        # Take the value from file_name and put it in a new key called 'video_id'
        if "file_name" in entry:
            entry["video_id"] = entry["file_name"]
            
        f_out.write(json.dumps(entry) + "\n")

print("✅ New metadata created with 'video_id' column for display.")