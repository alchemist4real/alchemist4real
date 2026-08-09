import json

with open("scripts/github_repos.json", "r", encoding="utf-8") as f:
    gh_repos = json.load(f)

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

vercel_map = {
    "alchemist4real": "https://alchemist4real.vercel.app",
    "markitdowninweb": "https://markitdowninweb.vercel.app",
    "mr-capsules": "https://mr-capsules.vercel.app",
    "phd-bioengineering-roadmap": "https://phd-bioengineering-roadmap.vercel.app",
    "sehatin-booth": "https://sehatin-booth.vercel.app",
    "gitrouter": "https://gitrouter-one.vercel.app",
    "dr.-been": "https://dr-been.vercel.app",
    "dr-been": "https://dr-been.vercel.app",
    "doctortablet": "https://doctortablet.vercel.app",
    "sartono": "https://sartono.vercel.app",
    "beencrypted": "https://beencrypted.vercel.app",
    "crypto-vault": "https://crypto-vault-livid-rho.vercel.app",
    "174": "https://174-three.vercel.app",
    "174-three": "https://174-three.vercel.app",
    "cookwithalchemist4real": "https://cookwithalchemist4real.vercel.app",
    "hipertensimengintaigenz": "https://hipertensimengintaigenz.vercel.app",
    "dermamaxxing": "https://dermamaxxing.vercel.app",
    "soyproteinbyaltaf": "https://soyproteinbyaltaf.vercel.app",
    "prisma-rdk-guide": "https://prisma-rdk-guide.vercel.app",
    "prisma-rdk-simulator": "https://prisma-rdk-simulator.vercel.app",
    "msgfromoracle": "https://msgfromoracle.vercel.app",
    "nosmoke": "https://nosmoke-six.vercel.app",
    "beentexter": "https://beentexter.vercel.app",
    "beenboxd": "https://beenboxd.vercel.app",
    "beenhollow": "https://beenhollow.vercel.app",
    "beencode": "https://beencode.vercel.app",
    "aetherial": "https://aetherial-beta.vercel.app",
    "zenlimitless": "https://zenlimitless.vercel.app",
    "saynotodrugs": "https://saynotodrugs-two.vercel.app",
    "fuckallrapist": "https://fuckallrapist.vercel.app",
    "saynotocholestrol": "https://saynotocholestrol.vercel.app"
}

print("=== ALL GITHUB REPOS ===")
for r in gh_repos:
    name = r["name"]
    name_clean = name.lower().replace("_", "-")
    ver_link = vercel_map.get(name_clean) or vercel_map.get(name.lower()) or r.get("homepage")
    desc = r.get("description") or "No description"
    print(f"Repo: {name} | Live: {ver_link} | Repo: {r['html_url']}")

