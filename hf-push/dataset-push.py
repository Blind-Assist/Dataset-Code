# from huggingface_hub import HfApi, login

# hf_token = "" 
# login(token=hf_token)

# api = HfApi()
# repo_id = "blind-assist/walk"

# print(f"🚀 Starting upload to {repo_id}...")

# # Upload the test folder 
# api.upload_folder(
#     folder_path="./test",    
#     path_in_repo="test",     
#     repo_id=repo_id,
#     repo_type="dataset",
#     # This keeps you informed if the upload is slow
#     # commit_message="Initial upload of test split videos and metadata"
#     # --- ADD THESE TWO LINES ---
#     multi_commits=True,           # Resumable and avoids 403/Timeout errors
#     multi_commits_verbose=True    # Shows you progress for every single file
# )

# print(f"✅ Test split uploaded successfully!")
# print(f"🔗 Check it here: https://huggingface.co/datasets/{repo_id}")

# from huggingface_hub import HfApi, login

# hf_token = "" 
# login(token=hf_token)
# api = HfApi()

# api.upload_file(
#     path_or_fileobj="test/metadata.jsonl",
#     path_in_repo="test/metadata.jsonl", # Keep the name standard in the repo
#     repo_id="blind-assist/walk",
#     repo_type="dataset"
# )


import os
from huggingface_hub import HfApi, login

hf_token = "" 
login(token=hf_token)

api = HfApi()
repo_id = "blind-assist/walk-train"

print(f"🚀 Starting LOCAL upload of 20GB to {repo_id}...")

# 2. Upload the TRAIN folder
api.upload_folder(
    folder_path="./train",    
    path_in_repo="train",     
    repo_id=repo_id,
    repo_type="dataset",
    multi_commits=True,           # Prevents "too many files" error
    multi_commits_verbose=True,   # Shows progress for each video
)

print(f"✅ Training split uploaded successfully!")