import os
import json
import time
import google.generativeai as genai

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH_DIR = os.path.join(BASE_DIR, "research")
DATA_FILE = os.path.join(BASE_DIR, "data.json")
KEYS_FILE = r"D:\DOWNLOAD\api_keys_collection.json"

# Load API Key
try:
    with open(KEYS_FILE, "r") as f:
        keys = json.load(f)
        gemini_keys = keys.get("GEMINI_API_KEYS", [])
        if not gemini_keys:
            print("No Gemini API keys found.")
            exit(1)
        # Using the first key
        genai.configure(api_key=gemini_keys[0])
except Exception as e:
    print(f"Failed to load API keys: {e}")
    exit(1)

def init_model():
    # Use flash for fast processing, or pro for better reasoning
    return genai.GenerativeModel('gemini-2.5-flash')

def extract_metadata(file_path):
    print(f"Uploading and processing {file_path}...")
    try:
        # Upload file to Gemini
        uploaded_file = genai.upload_file(path=file_path)
        
        model = init_model()
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
        if text.startswith('```json'):
            text = text[7:]
        if text.endswith('```'):
            text = text[:-3]
        text = text.strip()
        
        data = json.loads(text)
        
        # Cleanup file from Gemini servers to save space
        genai.delete_file(uploaded_file.name)
        
        return data
    except Exception as e:
        print(f"Failed to extract metadata for {file_path}: {e}")
        return None

def main():
    if not os.path.exists(RESEARCH_DIR):
        print(f"Research directory not found: {RESEARCH_DIR}")
        return

    # Load existing data
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
            continue # Already processed
            
        file_path = os.path.join(RESEARCH_DIR, filename)
        metadata = extract_metadata(file_path)
        
        if metadata:
            # Create new entry
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
            time.sleep(2) # Rate limit protection

    if new_files_processed > 0:
        with open(DATA_FILE, "w") as f:
            json.dump(db, f, indent=2)
        print(f"Saved {new_files_processed} new research entries to data.json")
    else:
        print("No new research files to process.")

if __name__ == "__main__":
    main()
