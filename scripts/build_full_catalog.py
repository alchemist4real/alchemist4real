import json

with open("scripts/github_repos.json", "r", encoding="utf-8") as f:
    gh_repos = json.load(f)

with open("data.json", "r", encoding="utf-8") as f:
    existing_data = json.load(f)

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

gh_map = {}
for r in gh_repos:
    name_clean = r["name"].lower().replace("_", "-").replace(".", "-")
    gh_map[name_clean] = r
    gh_map[r["name"].lower()] = r

print("=== NEW REPOS NOT IN CURRENT PROJECTS ===")
existing_titles = [p["title"].lower() for p in existing_data.get("projects", [])]
existing_links = [p.get("link", "").lower().rstrip("/") for p in existing_data.get("projects", [])]

for r in gh_repos:
    name = r["name"]
    name_clean = name.lower().replace("_", "-").replace(".", "-")
    homepage = r.get("homepage") or ""
    repo_url = r["html_url"]
    
    # Check if in existing projects
    matched = False
    for p in existing_data["projects"]:
        if p["title"].lower() == name.lower() or (p.get("repo_link") and p["repo_link"].lower() == repo_url.lower()):
            matched = True
            break
        if homepage and p.get("link", "").lower().rstrip("/") == homepage.lower().rstrip("/"):
            matched = True
            break
            
    if not matched:
        print(f"NEW REPO: {name} | Description: {r.get('description')} | Language: {r.get('language')} | Homepage: {homepage}")

print("\n=== VERCEL PROJECTS NOT IN CURRENT PROJECTS ===")
for v in vercel_projects:
    v_url = v["url"].lower().rstrip("/")
    matched = False
    for p in existing_data["projects"]:
        p_url = p.get("link", "").lower().rstrip("/")
        if p_url == v_url or p["title"].lower().replace(" ", "") == v["name"].lower().replace("-", ""):
            matched = True
            break
    if not matched and v["name"] != "alchemist4real":
        print(f"NEW VERCEL PROJECT: {v['name']} | Live: {v['url']}")

