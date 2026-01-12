import json
import os
import shutil

# --- Configuration (Based on your input) ---
JSON_FILE = r'D:\EE Semester 7\Design Project\test_alter_v2_fixed.json'
SOURCE_DIR = r'D:\EE Semester 7\Design Project\wad_dataset_v2\src_data'
DESTINATION_DIR = 'Selected_Metadata' 
# --- End Configuration ---

def copy_selected_metadata(json_file, source_dir, dest_dir):
    """
    Reads frame_path values from JSON and copies the corresponding 
    folders/files from source to a new destination folder.
    """
    
    # --- Step 1: Load and Parse JSON Data ---
    try:
        with open(json_file, 'r') as f:
            video_records = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: JSON file not found at '{json_file}'")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error: Could not parse JSON file '{json_file}'. Error details: {e}")
        return

    # Extract the unique frame_path names
    metadata_names = {record.get('frame_path') 
                      for record in video_records 
                      if isinstance(record, dict) and record.get('frame_path')}
    
    # --- Step 2: Prepare Destination Folder ---
    os.makedirs(dest_dir, exist_ok=True)
    
    copied_count = 0
    missing_count = 0

    print(f"🖼️ Starting metadata copy process...")
    print(f"Total unique metadata items to find: {len(metadata_names)}")
    print(f"Source Directory: {source_dir}")
    print(f"Destination Directory: {os.path.abspath(dest_dir)}\n")

    # --- Step 3: Iterate and Copy Metadata ---
    for item_name in metadata_names:
        source_path = os.path.join(source_dir, item_name)
        destination_path = os.path.join(dest_dir, item_name)

        if os.path.exists(source_path):
            try:
                if os.path.isdir(source_path):
                    # If it's a folder, use shutil.copytree for recursive copy
                    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
                else:
                    # If it's a file, use shutil.copy2
                    shutil.copy2(source_path, destination_path)
                
                copied_count += 1
            except Exception as e:
                print(f"⚠️ Failed to copy {item_name}: {e}")
        else:
            missing_count += 1

    # --- Step 4: Summary ---
    print("\n--- Summary ---")
    print(f"✅ Successfully copied **{copied_count}** metadata folders/files.")
    print(f"🚫 **{missing_count}** metadata items listed in JSON were not found in the source directory.")
    print(f"Your selected metadata is now in the folder: **{os.path.abspath(dest_dir)}**")

# Run the function
copy_selected_metadata(JSON_FILE, SOURCE_DIR, DESTINATION_DIR)