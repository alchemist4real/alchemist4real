import os
import json
import time
import urllib.request
import base64

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
    
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()[:4000]
    except Exception as e:
        print(f"[HF Fallback] Failed to read file: {e}")
        return None
        
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

    data = json.dumps({"inputs": prompt, "parameters": {"max_new_tokens": 150}}).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, headers={
        "Authorization": f"Bearer {hf_key}",
        "Content-Type": "application/json"
    })
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            generated_text = result[0].get("generated_text", "")
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
    try:
        with open(file_path, "rb") as f:
            file_data = f.read()
    except Exception as e:
        print(f"[Gemini] Failed to read file: {e}")
        return None
        
    ext = os.path.splitext(file_path)[1].lower()
    mime_map = {
        '.pdf': 'application/pdf',
        '.md': 'text/plain',
        '.txt': 'text/plain',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png'
    }
    mime_type = mime_map.get(ext, 'text/plain')
    
    encoded_data = base64.b64encode(file_data).decode('utf-8')
    prompt = """You are an expert AI data extractor and research assistant.
Analyze the attached document and generate a JSON object with the following structure:
{
  "title": "A catchy, uppercase title for this document (max 5 words)",
  "description": "A brief, one-sentence lowercase description of what this document is about.",
  "tags": ["Tag1", "Tag2", "Tag3"]
}
Do not include any markdown formatting like ```json or ``` in your response, just the raw JSON string. Make sure the output is perfectly valid JSON. Keep tags brief (1-2 words max, capitalize first letter)."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": mime_type, "data": encoded_data}}
            ]
        }]
    }
    
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            text = result['candidates'][0]['content']['parts'][0]['text'].strip()
            if text.startswith('```json'): text = text[7:]
            if text.endswith('```'): text = text[:-3]
            return json.loads(text.strip())
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode()
        raise Exception(f"HTTP {e.code}: {error_msg}")

def extract_metadata(file_path):
    print(f"\nProcessing {file_path}...")
    
    # Try all Gemini keys in sequence (Tier 1 & 2)
    for i, key in enumerate(gemini_keys):
        print(f"-> Attempting Gemini API Key {i+1}...")
        try:
            data = gemini_extract(file_path, key)
            if data: return data, f"Gemini (Key {i+1})"
        except Exception as e:
            print(f"   [Gemini Key {i+1} Failed]: {e}")
            time.sleep(1) # brief pause before rotation
            
    # Fallback to HuggingFace (Tier 3)
    print("-> All Gemini keys exhausted. Falling back to HuggingFace API...")
    hf_data = hf_extract(file_path)
    if hf_data: return hf_data, "HuggingFace"
    
    print("-> All AI processing tiers failed for this file.")
    return None, "FAILED"

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

    last_provider = "NONE"

    for filename in os.listdir(RESEARCH_DIR):
        if not filename.lower().endswith(supported_extensions):
            continue
        if filename in existing_files:
            continue
            
        file_path = os.path.join(RESEARCH_DIR, filename)
        metadata, provider = extract_metadata(file_path)
        
        if metadata:
            last_provider = provider
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

    # --- Write Heartbeat Log ---
    from datetime import datetime
    heartbeat_path = os.path.join(BASE_DIR, "heartbeat.json")
    heartbeat_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "OPERATIONAL" if new_files_processed > 0 or last_provider == "NONE" else "DEGRADED",
        "provider": last_provider,
        "files_processed": new_files_processed,
        "total_research_files": len(db["research"])
    }
    with open(heartbeat_path, "w") as f:
        json.dump(heartbeat_data, f, indent=2)
    print(f"Heartbeat updated: {heartbeat_data['status']}")

if __name__ == "__main__":
    main()
