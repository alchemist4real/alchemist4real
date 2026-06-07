import os
import json
import time
import google.generativeai as genai
import requests

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH_DIR = os.path.join(BASE_DIR, "research")
DATA_FILE = os.path.join(BASE_DIR, "data.json")
KEYS_FILE = r"D:\DOWNLOAD\api_keys_collection.json"

# API Keys Configuration
gemini_keys = []
hf_key = os.environ.get("HUGGINGFACE_API_KEY", "").strip()

# Load GEMINI Keys from Env (comma-separated)
env_gemini = os.environ.get("GEMINI_API_KEYS")
if env_gemini:
    gemini_keys = [k.strip() for k in env_gemini.split(",") if k.strip()]

# Fallback: Load Local Keys if Environment is empty
if not gemini_keys or not hf_key:
    if os.path.exists(KEYS_FILE):
        try:
            with open(KEYS_FILE, "r") as f:
                keys = json.load(f)
                if not gemini_keys:
                    gemini_keys = keys.get("GEMINI_API_KEYS", [])
                if not hf_key:
                    hf_key = keys.get("HUGGINGFACE_API_KEY", "").strip()
        except Exception as e:
            print(f"Failed to read local keys: {e}")

def hf_extract(file_path):
    print(f"[HF Fallback] Using HuggingFace Inference API for {file_path}...")
    if not hf_key:
        print("[HF Fallback] Failed: HUGGINGFACE_API_KEY is missing.")
        return None
    
    # Read text content safely
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"[HF Fallback] Failed to read file: {e}")
        return None
        
    # Truncate to save tokens (HF models have smaller context limits via Inference API)
    content = content[:4000] 
    
    headers = {"Authorization": f"Bearer {hf_key}"}
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    
    prompt = f"""[INST] You are an expert AI data extractor. Analyze the document below and generate a JSON object with this EXACT structure:
{{
  "title": "UPPERCASE TITLE MAX 5 WORDS",
  "description": "one-sentence lowercase description.",
  "tags": ["Tag1", "Tag2"]
}}
Output ONLY valid JSON and nothing else.
Document:
{content}
[/INST]"""

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 150}})
        if response.status_code != 200:
            print(f"[HF Fallback] API Error {response.status_code}: {response.text}")
            return None
        
        result = response.json()
        generated_text = result[0].get("generated_text", "")
        # Remove the prompt part if included
        if "[/INST]" in generated_text:
            generated_text = generated_text.split("[/INST]")[-1]
            
        text = generated_text.strip()
        if text.startswith('```json'): text = text[7:]
        if text.endswith('```'): text = text[:-3]
        
        return json.loads(text.strip())
    except Exception as e:
        print(f"[HF Fallback] Exception occurred: {e}")
        return None

def gemini_extract(file_path, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Upload file to Gemini
    uploaded_file = genai.upload_file(path=file_path)
    prompt = """
    You are an expert AI data extractor and research assistant.
    Analyze the attached document and generate a JSON object with the following structure:
    {
      "title": "A catchy, uppercase title for this document (max 5 words)",
      "description": "A brief, one-sentence lowercase description of what this document is about.",
      "tags": ["Tag1", "Tag2", "Tag3"]
    }
    Do not include any markdown formatting like ```json or ``` in your response, just the raw JSON string. Make sure the output is perfectly valid JSON. Keep tags brief (1-2 words max, capitalize first letter).
    """
    response = model.generate_content([uploaded_file, prompt])
    
    # Clean response string
    text = response.text.strip()
    if text.startswith('```json'): text = text[7:]
    if text.endswith('```'): text = text[:-3]
    text = text.strip()
    
    data = json.loads(text)
    genai.delete_file(uploaded_file.name)
    return data

def extract_metadata(file_path):
    print(f"\nProcessing {file_path}...")
    
    # Try all Gemini keys in sequence (Tier 1 & 2)
    for i, key in enumerate(gemini_keys):
        print(f"-> Attempting Gemini API Key {i+1}...")
        try:
            data = gemini_extract(file_path, key)
            if data: return data
        except Exception as e:
            print(f"   [Gemini Key {i+1} Failed]: {e}")
            time.sleep(1) # brief pause before rotation
            
    # Fallback to HuggingFace (Tier 3)
    print("-> All Gemini keys exhausted. Falling back to HuggingFace API...")
    hf_data = hf_extract(file_path)
    if hf_data: return hf_data
    
    print("-> All AI processing tiers failed for this file.")
    return None

def main():
    if not gemini_keys and not hf_key:
        print("WARNING: No API keys found in environment and local fallback unavailable.")
        print("Skipping AI research synchronization to allow build to continue.")
        exit(0)

    if not os.path.exists(RESEARCH_DIR):
        print(f"Research directory not found: {RESEARCH_DIR}")
        return

    with open(DATA_FILE, "r") as f:
        db = json.load(f)
    
    if "research" not in db:
        db["research"] = []
    
    existing_files = [item.get("file_name") for item in db["research"]]
    supported_extensions = ('.pdf', '.docx', '.md', '.jpg', '.jpeg', '.png')
    new_files_processed = 0

    for filename in os.listdir(RESEARCH_DIR):
        if not filename.lower().endswith(supported_extensions):
            continue
        if filename in existing_files:
            continue
            
        file_path = os.path.join(RESEARCH_DIR, filename)
        metadata = extract_metadata(file_path)
        
        if metadata:
            new_id = f"R{len(db['research']) + 1:02d}"
            entry = {
                "id": new_id,
                "title": metadata.get("title", filename.upper()),
                "description": metadata.get("description", "a research file."),
                "tags": metadata.get("tags", ["Research"]),
                "file_name": filename
            }
            db["research"].append(entry)
            existing_files.append(filename)
            new_files_processed += 1
            print(f"Successfully processed: {filename}")
            time.sleep(2) 

    if new_files_processed > 0:
        with open(DATA_FILE, "w") as f:
            json.dump(db, f, indent=2)
        print(f"\nSaved {new_files_processed} new research entries to data.json")
    else:
        print("\nNo new research files to process.")

if __name__ == "__main__":
    main()
