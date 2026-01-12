import json
import os

JSON_FILE = r'D:\EE Semester 7\Design Project\train_v2_fixed_4000.json'
SOURCE_DIR = r'D:\EE Semester 7\Design Project\wad_dataset_v2\src_data'

with open(JSON_FILE, 'r', encoding='utf-8') as f:
    video_records = json.load(f)

video_filenames = {record.get('video') for record in video_records if isinstance(record, dict) and record.get('video')}

print("Missing video files:")
for filename in video_filenames:
    source_path = os.path.join(SOURCE_DIR, filename)
    if not os.path.exists(source_path):
        print(f"  - {filename}")