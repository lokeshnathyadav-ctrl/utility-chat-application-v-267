from huggingface_hub import HfApi
import os
hf_api_key = os.getenv('HF_TOKEN')
api = HfApi(token=HF_TOKEN)
api.upload_folder(
    folder_path = "deployment",
    repo_id = "Lokeshnathy/ChatBot-v-267",
    repo_type = "space"
)
