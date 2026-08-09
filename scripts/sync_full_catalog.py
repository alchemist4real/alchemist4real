import json
import os
import re

DATA_FILE = "data.json"

with open("scripts/github_repos.json", "r", encoding="utf-8") as f:
    gh_repos = json.load(f)

vercel_projects = [
    {"name": "alchemist4real", "url": "https://alchemist4real.vercel.app"},
    {"name": "markitdowninweb", "url": "https://markitdowninweb.vercel.app"},
    {"name": "mr-capsules", "url": "https://mr-capsules.vercel.app"},
    {"name": "phd-bioengineering-roadmap", "url": "https://phd-bioengineering-roadmap.vercel.app"},
    {"name": "sehatin-booth", "url": "https://sehatin-booth.vercel.app"},
    {"name": "gitrouter", "url": "https://gitrouter-one.vercel.app"},
    {"name": "dr.-been", "url": "https://dr-been.vercel.app"},
    {"name": "doctortablet", "url": "https://doctortablet.vercel.app"},
    {"name": "sartono", "url": "https://sartono.vercel.app"},
    {"name": "beencrypted", "url": "https://beencrypted.vercel.app"},
    {"name": "crypto-vault", "url": "https://crypto-vault-livid-rho.vercel.app"},
    {"name": "174-three", "url": "https://174-three.vercel.app"},
    {"name": "cookwithalchemist4real", "url": "https://cookwithalchemist4real.vercel.app"},
    {"name": "hipertensimengintaigenz", "url": "https://hipertensimengintaigenz.vercel.app"},
    {"name": "dermamaxxing", "url": "https://dermamaxxing.vercel.app"},
    {"name": "soyproteinbyaltaf", "url": "https://soyproteinbyaltaf.vercel.app"},
    {"name": "prisma-rdk-guide", "url": "https://prisma-rdk-guide.vercel.app"},
    {"name": "prisma-rdk-simulator", "url": "https://prisma-rdk-simulator.vercel.app"},
    {"name": "msgfromoracle", "url": "https://msgfromoracle.vercel.app"},
    {"name": "nosmoke", "url": "https://nosmoke-six.vercel.app"},
    {"name": "beentexter", "url": "https://beentexter.vercel.app"},
    {"name": "beenboxd", "url": "https://beenboxd.vercel.app"},
    {"name": "beenhollow", "url": "https://beenhollow.vercel.app"},
    {"name": "beencode", "url": "https://beencode.vercel.app"},
    {"name": "aetherial", "url": "https://aetherial-beta.vercel.app"},
    {"name": "zenlimitless", "url": "https://zenlimitless.vercel.app"},
    {"name": "saynotodrugs", "url": "https://saynotodrugs-two.vercel.app"},
    {"name": "fuckallrapist", "url": "https://fuckallrapist.vercel.app"},
    {"name": "saynotocholestrol", "url": "https://saynotocholestrol.vercel.app"}
]

# Map Vercel project names to live URLs
vercel_map = {}
for vp in vercel_projects:
    key = vp["name"].lower().replace("-", "").replace(".", "").replace("_", "")
    vercel_map[key] = vp["url"]

# Predefined curated projects list to maintain top quality titles, descriptions, and tags
curated_projects = [
    {
        "id": "01",
        "title": "NO SMOKE",
        "description": "a science-backed minimalist landing page addressing nicotine automaticity and urge regulation.",
        "tags": ["Anti-Smoking", "Bilingual", "Dark"],
        "link": "https://nosmoke-six.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/nosmoke"
    },
    {
        "id": "02",
        "title": "#SayNoToDrugs",
        "description": "pretest -> 5 NAPZA topics -> posttest -> certificate.",
        "tags": ["Anti-Drugs", "Certificate"],
        "link": "https://saynotodrugs-two.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/saynotodrugs"
    },
    {
        "id": "03",
        "title": "#FuckAllRapist",
        "description": "consent, UU TPKS, bystander 5D — no sugarcoating.",
        "tags": ["Anti-Violence", "Certificate"],
        "link": "https://fuckallrapist.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/fuckallrapist"
    },
    {
        "id": "04",
        "title": "174 ARCHIVE",
        "description": "an immersive, dark-themed digital archive and web-based desktop simulation.",
        "tags": ["Academic", "Supabase", "Spotify"],
        "link": "https://174-three.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/MR-CAPSULES"
    },
    {
        "id": "05",
        "title": "SEHATIN BOOTH",
        "description": "interactive community health screening kiosk and vitals tracker.",
        "tags": ["Healthcare", "Kiosk", "Public Health"],
        "link": "https://sehatin-booth.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/sehatin-booth"
    },
    {
        "id": "06",
        "title": "DR. BEEN",
        "description": "ai-powered clinical diagnostic assistant and medical knowledge agent.",
        "tags": ["AI", "Clinical", "Diagnostics"],
        "link": "https://dr-been.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/dr-been"
    },
    {
        "id": "07",
        "title": "DOCTOR TABLET",
        "description": "streamlined digital workspace for physicians and medical bedside consultations.",
        "tags": ["Medical", "Workspace", "EHR"],
        "link": "https://doctortablet.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/doctortablet"
    },
    {
        "id": "08",
        "title": "PHD BIOENGINEERING ROADMAP",
        "description": "interactive academic trajectory and curriculum guide for bioengineering & medical tech.",
        "tags": ["Academic", "Bioengineering", "Roadmap"],
        "link": "https://phd-bioengineering-roadmap.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/phd-bioengineering-roadmap"
    },
    {
        "id": "09",
        "title": "LONGLIFEHISTO",
        "description": "an interactive web-based histology simulator to practice microscopic slide identification.",
        "tags": ["Histology", "Medical", "Simulation"],
        "link": "https://longlifehisto.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/longlifehisto"
    },
    {
        "id": "10",
        "title": "PRISMA SIMULATOR",
        "description": "national antibiotic distribution monitoring and e-prescription validator powered by blockchain.",
        "tags": ["Healthcare", "Surveillance", "Indonesia"],
        "link": "https://prisma-rdk-simulator.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/prisma-rdk-simulator"
    },
    {
        "id": "11",
        "title": "SAY NO TO CHOLESTEROL",
        "description": "program edukasi interaktif tentang kolesterol dan manajemen gaya hidup.",
        "tags": ["Edukasi", "Kesehatan", "Kolesterol"],
        "link": "https://saynotocholestrol.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/saynotocholestrol"
    },
    {
        "id": "12",
        "title": "HIPERTENSI MENGINTAI GEN Z",
        "description": "interactive health education about hypertension for gen z.",
        "tags": ["Health", "Education", "Hypertension"],
        "link": "https://hipertensimengintaigenz.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/hipertensimengintaigenz"
    },
    {
        "id": "13",
        "title": "DERMAMAXXING",
        "description": "skin intelligence system for automated dermatology anamnesis and tailored product routines.",
        "tags": ["Dermatology", "Skincare", "System"],
        "link": "https://dermamaxxing.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/dermamaxxing"
    },
    {
        "id": "14",
        "title": "NUTRI SOY BY ALTAF",
        "description": "personalized ai nutrition coaching and habit tracking powered by physical product qr code redemptions.",
        "tags": ["AI", "Nutrition", "Coaching"],
        "link": "https://soyproteinbyaltaf.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/soyproteinbyaltaf"
    },
    {
        "id": "15",
        "title": "MARKITDOWN IN WEB",
        "description": "web-based multi-format document to markdown converter powered by Microsoft MarkItDown.",
        "tags": ["Markdown", "Converter", "Utility"],
        "link": "https://markitdowninweb.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/markitdowninweb"
    },
    {
        "id": "16",
        "title": "COOK WITH ALCHEMIST",
        "description": "unified masterclass web app and experimental recipe lab by @alchemist4real.",
        "tags": ["Web", "Application", "Masterclass"],
        "link": "https://cookwithalchemist4real.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/cookwithalchemist4real"
    },
    {
        "id": "17",
        "title": "AETHERIAL",
        "description": "a spatial cognition test and mental rotation exercise.",
        "tags": ["Spatial", "Cognition", "Game"],
        "link": "https://aetherial-beta.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/aetherial"
    },
    {
        "id": "18",
        "title": "SOEXSOEX",
        "description": "an ai-powered collaborative question bank utilizing gemini content validation.",
        "tags": ["AI", "Question Bank", "Education"],
        "link": "https://soexsoex.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/soexsoex"
    },
    {
        "id": "19",
        "title": "LIVE VOICE GEMINI",
        "description": "realtime voice conversations with gemini using web speech transcription.",
        "tags": ["Gemini", "Voice", "AI"],
        "link": "https://live-one-beta.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/live"
    },
    {
        "id": "20",
        "title": "MSG FROM ORACLE",
        "description": "the sarcastic ai oracle that feeds on your futile wishes, real-time news, and market odds.",
        "tags": ["Web", "Application", "Oracle"],
        "link": "https://msgfromoracle.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/msgfromoracle"
    },
    {
        "id": "21",
        "title": "BEENBOXD",
        "description": "an ai-powered letterboxd logger.",
        "tags": ["Letterboxd", "Logger", "Movies"],
        "link": "https://beenboxd.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/beenboxd"
    },
    {
        "id": "22",
        "title": "BEENTEXTER",
        "description": "a brutalist retro-calculator style text generator with tactile vintage web aesthetics.",
        "tags": ["Retro", "Calculator", "Text Gen"],
        "link": "https://beentexter.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/beentexter"
    },
    {
        "id": "23",
        "title": "BEENCODE",
        "description": "industrial matrix encoder terminal. raw edge.",
        "tags": ["Encoder", "Industrial", "Utility"],
        "link": "https://beencode.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/beencode"
    },
    {
        "id": "24",
        "title": "BEENHOLLOW",
        "description": "ephemeral p2p file and message sharing directly into the void.",
        "tags": ["P2P", "File Sharing", "Real-time"],
        "link": "https://beenhollow.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/BEENHOLLOW"
    },
    {
        "id": "25",
        "title": "LIMITLESS OMNIPRESENT",
        "description": "gojo satoru technique simulator with 100k gpu particles.",
        "tags": ["Simulator", "Mediapipe", "WebGL"],
        "link": "https://zenlimitless.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/zenlimitless"
    },
    {
        "id": "26",
        "title": "PRISMA RDK GUIDE",
        "description": "blockchain-powered health chain system documentation & guide.",
        "tags": ["Blockchain", "Healthcare", "Antibiotics"],
        "link": "https://prisma-rdk-guide.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/prisma-rdk-guide"
    }
]

curated_extensions = [
    {
        "id": "GH-TIM",
        "title": "TIMEMARU",
        "description": "a browser extension merging daily productivity tools with an interactive, screen-roaming pixel art demon.",
        "tags": ["Productivity", "Pixel Art", "Extension"],
        "link": "https://github.com/alchemist4real/timemaru"
    },
    {
        "id": "GH-OMN",
        "title": "OMNIFORM AUTOFILLER",
        "description": "GForm dominator with robust React-safe injection.",
        "tags": ["Extension", "JavaScript", "Automation"],
        "link": "https://github.com/alchemist4real/OmniForm-Autofiller"
    },
    {
        "id": "GH-PEE",
        "title": "PEERASSESS NINJA",
        "description": "Single-click peer assessment automation extension.",
        "tags": ["Extension", "JavaScript", "Automation"],
        "link": "https://github.com/alchemist4real/PeerAssess-Ninja"
    }
]

# Track existing repo links & titles to build repos list without duplicates
project_repo_links = set(p["repo_link"].lower().rstrip("/") for p in curated_projects if "repo_link" in p)
project_web_links = set(p["link"].lower().rstrip("/") for p in curated_projects if "link" in p)

repos_list = []

for r in gh_repos:
    html_url = r["html_url"].lower().rstrip("/")
    name = r["name"]
    name_clean = name.lower().replace("-", "").replace(".", "").replace("_", "")
    
    # Skip if extension
    if any(ext["link"].lower().rstrip("/") == html_url for ext in curated_extensions):
        continue
        
    live_link = vercel_map.get(name_clean) or r.get("homepage")
    
    repo_entry = {
        "id": "GH-" + name[:3].upper(),
        "title": name.upper().replace("-", " ").replace("_", " "),
        "description": r.get("description") or f"open source repository for {name}.",
        "tags": r.get("topics")[:2] if r.get("topics") else ([r.get("language")] if r.get("language") else ["Code"]),
        "link": r["html_url"]
    }
    if live_link:
        repo_entry["web_link"] = live_link
        
    repos_list.append(repo_entry)

new_data = {
    "projects": curated_projects,
    "extensions": curated_extensions,
    "research": [],
    "repos": repos_list
}

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(new_data, f, indent=2)

print(f"Successfully synced full catalog into data.json! Total projects: {len(curated_projects)}, Extensions: {len(curated_extensions)}, Repos: {len(repos_list)}")
