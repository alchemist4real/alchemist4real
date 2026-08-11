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
        "description": "science-backed landing page for nicotine urge regulation",
        "tags": ["Anti-Smoking", "Bilingual", "Dark"],
        "link": "https://nosmoke-six.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/nosmoke"
    },
    {
        "id": "02",
        "title": "#SayNoToDrugs",
        "description": "interactive drug education with pre/post-test & certificate",
        "tags": ["Anti-Drugs", "Certificate"],
        "link": "https://saynotodrugs-two.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/saynotodrugs"
    },
    {
        "id": "03",
        "title": "#FuckAllRapist",
        "description": "anti-sexual violence guide covering consent & bystander action",
        "tags": ["Anti-Violence", "Certificate"],
        "link": "https://fuckallrapist.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/fuckallrapist"
    },
    {
        "id": "04",
        "title": "174 ARCHIVE",
        "description": "dark-themed digital archive & desktop simulation",
        "tags": ["Academic", "Supabase", "Spotify"],
        "link": "https://174-three.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/MR-CAPSULES"
    },
    {
        "id": "05",
        "title": "SEHATIN BOOTH",
        "description": "community health screening kiosk & vitals tracker",
        "tags": ["Healthcare", "Kiosk", "Public Health"],
        "link": "https://sehatin-booth.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/sehatin-booth"
    },
    {
        "id": "06",
        "title": "DR. BEEN",
        "description": "ai clinical diagnostic assistant & medical knowledge agent",
        "tags": ["AI", "Clinical", "Diagnostics"],
        "link": "https://dr-been.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/dr-been"
    },
    {
        "id": "07",
        "title": "DOCTOR TABLET",
        "description": "digital workspace for bedside medical consultations",
        "tags": ["Medical", "Workspace", "EHR"],
        "link": "https://doctortablet.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/doctortablet"
    },
    {
        "id": "08",
        "title": "PHD BIOENGINEERING ROADMAP",
        "description": "academic trajectory guide for bioengineering & medtech",
        "tags": ["Academic", "Bioengineering", "Roadmap"],
        "link": "https://phd-bioengineering-roadmap.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/phd-bioengineering-roadmap"
    },
    {
        "id": "09",
        "title": "LONGLIFEHISTO",
        "description": "interactive histology simulator for slide identification",
        "tags": ["Histology", "Medical", "Simulation"],
        "link": "https://longlifehisto.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/longlifehisto"
    },
    {
        "id": "10",
        "title": "PRISMA SIMULATOR",
        "description": "blockchain antibiotic distribution & e-prescription validator",
        "tags": ["Healthcare", "Surveillance", "Indonesia"],
        "link": "https://prisma-rdk-simulator.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/prisma-rdk-simulator"
    },
    {
        "id": "11",
        "title": "SAY NO TO CHOLESTEROL",
        "description": "interactive cholesterol & lifestyle education",
        "tags": ["Edukasi", "Kesehatan", "Kolesterol"],
        "link": "https://saynotocholestrol.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/saynotocholestrol"
    },
    {
        "id": "12",
        "title": "HIPERTENSI MENGINTAI GEN Z",
        "description": "interactive hypertension health education for gen z",
        "tags": ["Health", "Education", "Hypertension"],
        "link": "https://hipertensimengintaigenz.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/hipertensimengintaigenz"
    },
    {
        "id": "13",
        "title": "DERMAMAXXING",
        "description": "skin intelligence system for dermatology anamnesis",
        "tags": ["Dermatology", "Skincare", "System"],
        "link": "https://dermamaxxing.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/dermamaxxing"
    },
    {
        "id": "14",
        "title": "NUTRI SOY BY ALTAF",
        "description": "ai nutrition coaching & qr habit tracker",
        "tags": ["AI", "Nutrition", "Coaching"],
        "link": "https://soyproteinbyaltaf.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/soyproteinbyaltaf"
    },
    {
        "id": "15",
        "title": "MARKITDOWN IN WEB",
        "description": "multi-format document to markdown converter",
        "tags": ["Markdown", "Converter", "Utility"],
        "link": "https://markitdowninweb.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/markitdowninweb"
    },
    {
        "id": "16",
        "title": "COOK WITH ALCHEMIST",
        "description": "masterclass web app & experimental recipe lab",
        "tags": ["Web", "Application", "Masterclass"],
        "link": "https://cookwithalchemist4real.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/cookwithalchemist4real"
    },
    {
        "id": "17",
        "title": "AETHERIAL",
        "description": "spatial cognition test & mental rotation exercise",
        "tags": ["Spatial", "Cognition", "Game"],
        "link": "https://aetherial-beta.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/aetherial"
    },
    {
        "id": "18",
        "title": "SOEXSOEX",
        "description": "ai collaborative question bank with gemini validation",
        "tags": ["AI", "Question Bank", "Education"],
        "link": "https://soexsoex.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/soexsoex"
    },
    {
        "id": "19",
        "title": "LIVE VOICE GEMINI",
        "description": "realtime voice conversations with gemini ai",
        "tags": ["Gemini", "Voice", "AI"],
        "link": "https://live-one-beta.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/live"
    },
    {
        "id": "20",
        "title": "MSG FROM ORACLE",
        "description": "sarcastic ai oracle feeding on news & market odds",
        "tags": ["Web", "Application", "Oracle"],
        "link": "https://msgfromoracle.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/msgfromoracle"
    },
    {
        "id": "21",
        "title": "BEENBOXD",
        "description": "ai-powered letterboxd movie logger",
        "tags": ["Letterboxd", "Logger", "Movies"],
        "link": "https://beenboxd.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/beenboxd"
    },
    {
        "id": "22",
        "title": "BEENTEXTER",
        "description": "brutalist retro-calculator style text generator",
        "tags": ["Retro", "Calculator", "Text Gen"],
        "link": "https://beentexter.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/beentexter"
    },
    {
        "id": "23",
        "title": "BEENCODE",
        "description": "industrial matrix encoder terminal",
        "tags": ["Encoder", "Industrial", "Utility"],
        "link": "https://beencode.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/beencode"
    },
    {
        "id": "24",
        "title": "BEENHOLLOW",
        "description": "ephemeral p2p file & message sharing",
        "tags": ["P2P", "File Sharing", "Real-time"],
        "link": "https://beenhollow.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/BEENHOLLOW"
    },
    {
        "id": "25",
        "title": "LIMITLESS OMNIPRESENT",
        "description": "gojo satoru technique simulator with gpu particles",
        "tags": ["Simulator", "Mediapipe", "WebGL"],
        "link": "https://zenlimitless.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/zenlimitless"
    },
    {
        "id": "26",
        "title": "PRISMA RDK GUIDE",
        "description": "blockchain health chain documentation & guide",
        "tags": ["Blockchain", "Healthcare", "Antibiotics"],
        "link": "https://prisma-rdk-guide.vercel.app/",
        "repo_link": "https://github.com/alchemist4real/prisma-rdk-guide"
    }
]

curated_extensions = [
    {
        "id": "GH-TIM",
        "title": "TIMEMARU",
        "description": "productivity extension with interactive pixel art demon",
        "tags": ["Productivity", "Pixel Art", "Extension"],
        "link": "https://github.com/alchemist4real/timemaru"
    },
    {
        "id": "GH-OMN",
        "title": "OMNIFORM AUTOFILLER",
        "description": "gform autofill extension with react-safe injection",
        "tags": ["Extension", "JavaScript", "Automation"],
        "link": "https://github.com/alchemist4real/OmniForm-Autofiller"
    },
    {
        "id": "GH-PEE",
        "title": "PEERASSESS NINJA",
        "description": "single-click peer assessment automation extension",
        "tags": ["Extension", "JavaScript", "Automation"],
        "link": "https://github.com/alchemist4real/PeerAssess-Ninja"
    }
]

curated_repo_descriptions = {
    "markitdowninweb": "open source web document to markdown converter",
    "mr-capsules": "medical student learning platform & digital archive",
    "cookwithalchemist4real": "masterclass web app & experimental recipe lab",
    "hipertensimengintaigenz": "hypertension health education web app for gen z",
    "saynotocholestrol": "interactive cholesterol & lifestyle education app",
    "fuckallrapist": "anti-sexual violence & consent education guide",
    "saynotodrugs": "interactive drug education & certification platform",
    "zenlimitless": "gojo satoru technique simulator with gpu particles",
    "aetherial": "spatial cognition test & mental rotation exercise",
    "beencode": "industrial matrix encoder terminal",
    "soyproteinbyaltaf": "ai nutrition coaching & qr habit tracker",
    "soexsoex": "ai collaborative question bank with gemini validation",
    "sinxv": "headless whatsapp ai assistant controlled via telegram",
    "saturday": "serverless ai assistant backend on cloudflare workers",
    "prisma-rdk-guide": "blockchain health chain system documentation & guide",
    "prisma-rdk-simulator": "blockchain antibiotic distribution & e-prescription validator",
    "soalganjilgenap": "odd-even speed accuracy test generator for psych exams",
    "monday": "minimalist chat app powered by cloudflare workers ai",
    "msgfromoracle": "sarcastic ai oracle feeding on news & market odds",
    "live": "realtime voice conversations with gemini ai",
    "longlifehisto": "interactive histology simulator for slide identification",
    "nosmoke": "science-backed landing page for nicotine urge regulation",
    "cosxouboros": "autonomous web entity that rewrites its code via ai",
    "beenonexamaccess": "decentralized web3 wallet protocol for exam access",
    "friday": "dark-mode personal ai assistant on cloudflare workers",
    "beentexter": "brutalist retro-calculator style text generator",
    "geminibeenspace": "guide for students to unlock free 1-year gemini trial",
    "beenboxd": "ai letterboxd movie logger & csv exporter",
    "academiccontrolcenter": "gamified academic dashboard for task tracking",
    "beenhollow": "ephemeral p2p file & message sharing",
    "beenmoney": "minimalist dark-themed single-file budgeting app"
}

def format_desc(text):
    if not text:
        return ""
    text = text.strip()
    for prefix in ["a ", "an ", "the ", "A ", "An ", "The "]:
        if text.startswith(prefix):
            text = text[len(prefix):]
            break
    text = text.lower().rstrip(". ")
    return text

# Exclude repos specified by user to avoid redundancy on web catalog
excluded_repo_names = {
    "cookwithalchemist4real", "zenlimitless", "soexsoex", "sinxv", "saturday",
    "prisma-rdk-simulator", "monday", "live", "longlifehisto", "cosxouboros",
    "beenonexamaccess", "friday", "geminibeenspace", "academiccontrolcenter", "beenmoney"
}

repos_list = []

for r in gh_repos:
    html_url = r["html_url"].lower().rstrip("/")
    name = r["name"]
    name_clean = name.lower().replace("-", "").replace(".", "").replace("_", "")
    
    # Skip if excluded or extension
    if name.lower() in excluded_repo_names:
        continue
    if any(ext["link"].lower().rstrip("/") == html_url for ext in curated_extensions):
        continue
        
    live_link = vercel_map.get(name_clean) or r.get("homepage")
    
    raw_desc = curated_repo_descriptions.get(name.lower()) or r.get("description") or f"open source repository for {name}"
    
    repo_entry = {
        "id": "GH-" + name[:3].upper(),
        "title": name.upper().replace("-", " ").replace("_", " "),
        "description": format_desc(raw_desc),
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

