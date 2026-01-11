import json

with open("train_alter.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("train/metadata.jsonl", "w", encoding="utf-8") as f:
    for entry in data:
        # We rename 'video' to 'file_name' so the HF UI recognizes it
        entry["file_name"] = entry.pop("video") 
        f.write(json.dumps(entry) + "\n")