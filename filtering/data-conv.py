import json
import os
import shutil

# --- Configuration (UPDATED) ---
# 1. Path to your JSON file
# Note: Using your specified path
JSON_FILE = r'D:\EE Semester 7\Design Project\train_v2_fixed_alter.json'

# 2. Path to the folder containing ALL your video files
# Note: Using your specified path
SOURCE_DIR = r'D:\EE Semester 7\Design Project\wad_dataset_v2\src_data'

# 3. Name for the new folder to hold the selected videos.
# This folder will be created in the current directory where you run the script.
DESTINATION_DIR = 'Selected_Videos_train'
# --- End Configuration ---

def copy_selected_videos(json_file, source_dir, dest_dir):
    """Reads video names from JSON and copies them from source to destination."""
    
    # --- Step 1: Load and Parse JSON Data ---
    try:
        # The data you provided looked like a list of dictionaries, but without
        # the enclosing brackets []. We will attempt to load it as one large
        # string and parse each line as a separate JSON object if needed.
        # However, assuming your actual file is a valid JSON array or object:
        with open(json_file, 'r', encoding='utf-8') as f:
            # We assume the file contains a valid JSON array of objects.
            video_records = json.load(f)
            
    except FileNotFoundError:
        print(f"❌ Error: JSON file not found at '{json_file}'")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error: Could not parse JSON file '{json_file}'. Check its format. Error details: {e}")
        return
    
    # Extract the filenames. We assume 'video' is the key holding the filename.
    video_filenames = {record.get('video') for record in video_records if isinstance(record, dict) and record.get('video')}
    
    # --- Step 2: Prepare Destination Folder ---
    # Create the destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)
    
    copied_count = 0
    missing_count = 0

    print(f"🎬 Starting file copy process...")
    print(f"Total unique videos to copy: {len(video_filenames)}")
    print(f"Source Directory: {source_dir}")
    print(f"Destination Directory: {os.path.abspath(dest_dir)}\n")

    # --- Step 3: Iterate and Copy Files ---
    for filename in video_filenames:
        source_path = os.path.join(source_dir, filename)
        destination_path = os.path.join(dest_dir, filename)

        if os.path.exists(source_path):
            try:
                # Use copy2 to preserve metadata (timestamps, etc.)
                shutil.copy2(source_path, destination_path)
                copied_count += 1
            except Exception as e:
                print(f"⚠️ Failed to copy {filename}: {e}")
        else:
            missing_count += 1
            # Optional: Uncomment the line below to see which files were missing
            print(f"🚫 Missing: {filename}")

    # --- Step 4: Summary ---
    print("\n--- Summary ---")
    print(f"✅ Successfully copied **{copied_count}** video files.")
    print(f"🚫 **{missing_count}** video files listed in JSON were not found in the source directory.")
    print(f"Your selected videos are now in the folder: **{os.path.abspath(dest_dir)}**")

# Run the function
copy_selected_videos(JSON_FILE, SOURCE_DIR, DESTINATION_DIR)