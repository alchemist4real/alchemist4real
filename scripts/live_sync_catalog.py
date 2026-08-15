import urllib.request
import json
import os
from datetime import datetime

VERCEL_DEPLOYMENTS = {
    "alchemist4real": "https://alchemist4real.vercel.app",
    "beenhollow": "https://beenhollow.vercel.app",
    "photoboothapp-maple2026": "https://photoboothapp-maple2026.vercel.app",
    "markitdowninweb": "https://markitdowninweb.vercel.app",
    "mr-capsules": "https://mr-capsules.vercel.app",
    "soyproteinbyaltaf": "https://soyproteinbyaltaf.vercel.app",
    "prisma-rdk-guide": "https://prisma-rdk-guide.vercel.app",
    "msgfromoracle": "https://msgfromoracle.vercel.app",
    "nosmoke": "https://nosmoke-six.vercel.app",
    "beentexter": "https://beentexter.vercel.app",
    "beenboxd": "https://beenboxd.vercel.app",
    "hipertensimengintaigenz": "https://hipertensimengintaigenz.vercel.app",
    "saynotocholestrol": "https://saynotocholestrol.vercel.app",
    "fuckallrapist": "https://fuckallrapist.vercel.app",
    "saynotodrugs": "https://saynotodrugs-two.vercel.app",
    "aetherial": "https://aetherial-beta.vercel.app",
    "beencode": "https://beencode.vercel.app",
    "phd-bioengineering-roadmap": "https://phd-bioengineering-roadmap.vercel.app",
    "doctortablet": "https://doctortablet.vercel.app",
    "dr-been": "https://dr-been.vercel.app",
    "dermamaxxing": "https://dermamaxxing.vercel.app",
    "cookwithalchemist4real": "https://cookwithalchemist4real.vercel.app",
    "zenlimitless": "https://zenlimitless.vercel.app",
}

STANDARDIZED_DESCRIPTIONS = {
    "beenhollow": "ephemeral p2p file & real-time message sharing",
    "photoboothapp-maple2026": "interactive digital photobooth & event photo app",
    "markitdowninweb": "multi-format document to markdown web converter",
    "mr-capsules": "comprehensive medical study platform & lecture archive",
    "omniform-autofiller": "google forms autofill extension with react-safe injection",
    "peerassess-ninja": "google forms automation tool for peer assessments",
    "hipertensimengintaigenz": "interactive hypertension education platform for gen z",
    "saynotocholestrol": "interactive cholesterol & cardiovascular education",
    "fuckallrapist": "anti-sexual violence & bystander action guide",
    "saynotodrugs": "interactive drug education & certification simulator",
    "aetherial": "spatial cognition assessment & mental rotation exercise",
    "beencode": "industrial matrix encoder & terminal utility",
    "soyproteinbyaltaf": "ai nutrition coach & qr redemption habit tracker",
    "timemaru": "productivity suite with interactive pixel art demon",
    "prisma-rdk-guide": "blockchain prescription verification architecture",
    "soalganjilgenap": "odd-even speed accuracy test generator for psych exams",
    "msgfromoracle": "sarcastic ai oracle analyzing news & market odds",
    "nosmoke": "nicotine urge regulation & cessation landing page",
    "beentexter": "tactile retro-calculator style text generator",
    "beenboxd": "ai-assisted letterboxd movie logger & exporter",
    "alchemist4real": "portfolio architecture, identity card & brutalist core",
    "phd-bioengineering-roadmap": "academic trajectory roadmap for bioengineering & medtech",
    "doctortablet": "digital clinical workspace for bedside medical consults",
    "dr-been": "ai clinical diagnostic assistant & medical agent",
    "dermamaxxing": "skin intelligence system for dermatology anamnesis",
    "cookwithalchemist4real": "culinary masterclass app & experimental recipe lab",
    "zenlimitless": "interactive gpu particle physics visual simulation"
}

CUSTOM_TAGS = {
    "beenhollow": ["P2P", "File-Sharing", "Real-Time"],
    "photoboothapp-maple2026": ["Photobooth", "Canvas-API", "CIMSA"],
    "markitdowninweb": ["Markdown", "Converter", "Utility"],
    "mr-capsules": ["Medical", "Platform", "Archive"],
    "omniform-autofiller": ["Chrome-Extension", "GForm", "Automation"],
    "peerassess-ninja": ["Chrome-Extension", "Automation", "Education"],
    "hipertensimengintaigenz": ["Health", "Hypertension", "Gen-Z"],
    "saynotocholestrol": ["Education", "Health", "Cardiology"],
    "fuckallrapist": ["Anti-Violence", "Consent", "Guide"],
    "saynotodrugs": ["Anti-Drugs", "Education", "Certificate"],
    "aetherial": ["Spatial", "Cognition", "Neuro"],
    "beencode": ["Encoder", "Matrix", "Terminal"],
    "soyproteinbyaltaf": ["AI", "Nutrition", "Coaching"],
    "timemaru": ["Extension", "Productivity", "Pixel-Art"],
    "prisma-rdk-guide": ["Blockchain", "Healthcare", "AMR"],
    "soalganjilgenap": ["Psychology", "Testing", "Tool"],
    "msgfromoracle": ["AI-Oracle", "News", "Market-Odds"],
    "nosmoke": ["Anti-Smoking", "Bilingual", "Health"],
    "beentexter": ["Retro", "Typography", "Generator"],
    "beenboxd": ["Letterboxd", "AI", "Movies"],
    "alchemist4real": ["Identity", "Portfolio", "Brutalist"],
    "phd-bioengineering-roadmap": ["Bioengineering", "Academic", "Roadmap"],
    "doctortablet": ["Medical", "Workspace", "EHR"],
    "dr-been": ["AI", "Clinical", "Diagnostics"],
    "dermamaxxing": ["Dermatology", "Skincare", "Anamnesis"],
    "cookwithalchemist4real": ["Masterclass", "Lab", "Culinary"],
    "zenlimitless": ["GPU-Particles", "Simulation", "Interactive"]
}

def sync():
    print("Fetching latest repos from GitHub API...")
    req = urllib.request.Request(
        'https://api.github.com/users/alchemist4real/repos?per_page=100&sort=updated',
        headers={'User-Agent': 'alchemist4real-sync'}
    )
    
    try:
        with urllib.request.urlopen(req) as res:
            repos = json.loads(res.read().decode('utf-8'))
    except Exception as e:
        print("Error fetching from GitHub:", e)
        if os.path.exists('scripts/github_repos.json'):
            with open('scripts/github_repos.json', 'r', encoding='utf-8') as f:
                repos = json.load(f)
        else:
            return

    # Sort repos by updated_at descending
    repos.sort(key=lambda r: r.get('updated_at', ''), reverse=True)

    projects_list = []
    extensions_list = []
    repos_list = []

    project_counter = 1

    for r in repos:
        name = r.get('name', '')
        name_key = name.lower()
        
        # Determine live web link
        web_link = r.get('homepage')
        if not web_link or web_link == "":
            web_link = VERCEL_DEPLOYMENTS.get(name_key, "")
        
        repo_link = r.get('html_url', f"https://github.com/alchemist4real/{name}")
        
        # Clean title
        title = name.upper().replace("-", " ").replace("_", " ")
        if name_key == "photoboothapp-maple2026":
            title = "PHOTOBOOTH APP MAPLE 2026"
        elif name_key == "mr-capsules":
            title = "MR CAPSULES"
        elif name_key == "markitdowninweb":
            title = "MARKITDOWN IN WEB"
        elif name_key == "hipertensimengintaigenz":
            title = "HIPERTENSI MENGINTAI GEN Z"
        elif name_key == "saynotocholestrol":
            title = "SAY NO TO CHOLESTEROL"
        elif name_key == "omniform-autofiller":
            title = "OMNIFORM AUTOFILLER"
        elif name_key == "peerassess-ninja":
            title = "PEERASSESS NINJA"
        elif name_key == "saynotodrugs":
            title = "#SayNoToDrugs"
        elif name_key == "fuckallrapist":
            title = "#FuckAllRapist"
        elif name_key == "soyproteinbyaltaf":
            title = "NUTRI SOY BY ALTAF"
        elif name_key == "soalganjilgenap":
            title = "SOAL GANJIL GENAP"
        elif name_key == "msgfromoracle":
            title = "MSG FROM ORACLE"

        # Standardized description
        desc = STANDARDIZED_DESCRIPTIONS.get(
            name_key,
            (r.get('description') or f"open source {name} project").lower().rstrip('.')
        )

        # Tags
        tags = CUSTOM_TAGS.get(
            name_key,
            r.get('topics')[:3] if r.get('topics') else ([r.get('language')] if r.get('language') else ["Code"])
        )

        # Determine type
        is_ext = (
            "extension" in name_key or
            "autofill" in name_key or
            "timemaru" in name_key or
            "ninja" in name_key or
            (r.get('description') and "extension" in r.get('description', '').lower())
        )

        if is_ext:
            extensions_list.append({
                "id": f"EXT-{len(extensions_list)+1:02d}",
                "title": title,
                "description": desc,
                "tags": tags,
                "link": web_link if web_link else repo_link,
                "repo_link": repo_link
            })
        else:
            # Has a live web deployment?
            if web_link:
                projects_list.append({
                    "id": f"{project_counter:02d}",
                    "title": title,
                    "description": desc,
                    "tags": tags,
                    "link": web_link,
                    "repo_link": repo_link
                })
                project_counter += 1
            else:
                repos_list.append({
                    "id": f"GH-{name[:3].upper()}",
                    "title": title,
                    "description": desc,
                    "tags": tags,
                    "link": repo_link,
                    "repo_link": repo_link
                })

    # Add standalone deployed projects not currently having a public GitHub repo (if any)
    standalone_projects = [
        ("dr-been", "DR. BEEN", "ai clinical diagnostic assistant & medical agent", ["AI", "Clinical", "Diagnostics"], "https://dr-been.vercel.app/"),
        ("doctortablet", "DOCTOR TABLET", "digital clinical workspace for bedside medical consults", ["Medical", "Workspace", "EHR"], "https://doctortablet.vercel.app/"),
        ("phd-bioengineering-roadmap", "PHD BIOENGINEERING ROADMAP", "academic trajectory roadmap for bioengineering & medtech", ["Academic", "Bioengineering", "Roadmap"], "https://phd-bioengineering-roadmap.vercel.app/"),
        ("longlifehisto", "LONGLIFEHISTO", "interactive histology simulator for tissue identification", ["Histology", "Medical", "Simulation"], "https://longlifehisto.vercel.app/"),
        ("dermamaxxing", "DERMAMAXXING", "skin intelligence system for dermatology anamnesis", ["Dermatology", "Skincare", "System"], "https://dermamaxxing.vercel.app/"),
        ("cookwithalchemist4real", "COOK WITH ALCHEMIST", "culinary masterclass app & experimental recipe lab", ["Masterclass", "Lab", "Culinary"], "https://cookwithalchemist4real.vercel.app/"),
        ("zenlimitless", "LIMITLESS OMNIPRESENT", "interactive gpu particle physics visual simulation", ["GPU-Particles", "Simulation", "Interactive"], "https://zenlimitless.vercel.app/"),
        ("174-three", "174 ARCHIVE", "dark brutalist digital archive & desktop simulation", ["Academic", "Supabase", "Spotify"], "https://174-three.vercel.app/")
    ]

    existing_titles = [p["title"].lower() for p in projects_list]
    for key, stitle, sdesc, stags, slink in standalone_projects:
        if stitle.lower() not in existing_titles and key not in [r.get('name', '').lower() for r in repos]:
            projects_list.append({
                "id": f"{project_counter:02d}",
                "title": stitle,
                "description": sdesc,
                "tags": stags,
                "link": slink,
                "repo_link": f"https://github.com/alchemist4real/{key}"
            })
            project_counter += 1

    final_data = {
        "projects": projects_list,
        "extensions": extensions_list,
        "research": [],
        "repos": repos_list
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2)

    print(f"Live GitHub Catalog Sync Complete:")
    print(f"- Projects: {len(projects_list)}")
    for p in projects_list[:10]:
        print(f"  [{p['id']}] {p['title']} ({p['link']})")
    print(f"- Extensions: {len(extensions_list)}")
    print(f"- Repos: {len(repos_list)}")

if __name__ == '__main__':
    sync()
