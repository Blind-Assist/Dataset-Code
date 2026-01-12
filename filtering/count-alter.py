import json

def count_alter_objects(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total = len(data)
    with_alter = sum(1 for obj in data if 'alter' in obj and obj['alter'])
    without_alter = total - with_alter
    
    print(f"Total objects: {total}")
    print(f"Objects with 'alter': {with_alter}")
    print(f"Objects without 'alter' (empty): {without_alter}")

if __name__ == "__main__":
    count_alter_objects(r"d:\EE Semester 7\Design Project\train_v2_fixed.json")