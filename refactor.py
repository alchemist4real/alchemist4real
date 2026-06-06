import re

with open(r"d:\DOWNLOAD\alchemist4real\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Change :root CSS variables
html = re.sub(r"--bg:\s*#[0-9a-fA-F]+;", "--bg: #ffffff;", html)
html = re.sub(r"--bg2:\s*#[0-9a-fA-F]+;", "--bg2: #fcfcfc;", html)
html = re.sub(r"--surface:\s*#[0-9a-fA-F]+;", "--surface: #ffffff;", html)
html = re.sub(r"--surface2:\s*#[0-9a-fA-F]+;", "--surface2: #f8f8f8;", html)
html = re.sub(r"--border:\s*#?[0-9a-fA-F]+;", "--border: #e0e0e0;", html)
html = re.sub(r"--text:\s*#[0-9a-fA-F]+;", "--text: #111111;", html)
html = re.sub(r"--text-dim:\s*#?[0-9a-fA-F]+;", "--text-dim: #666666;", html)

# 2. Remove body::after scanlines (set background to none)
html = re.sub(r"(body::after\s*\{[^}]*background:)\s*repeating-linear-gradient[^;]+;", r"\1 none;", html)

# 3. Change .section and .about-inner max-widths to 800px (from 1000px)
html = re.sub(r"(\.section\s*\{[^}]*max-width:\s*)1000px", r"\g<1>800px", html)
html = re.sub(r"(\.about-inner\s*\{[^}]*max-width:\s*)1000px", r"\g<1>800px", html)

# 4. Change .project-card-inner min-height to 180px (from 320px)
html = re.sub(r"(\.project-card-inner\s*\{[^}]*min-height:\s*)320px", r"\g<1>180px", html)

# 5. Consolidate WA Links
html = re.sub(r"https://wa\.me/\d+", "https://wa.me/6285778120332", html)

# Delete WA Partner div
wa_partner_pattern = r"<!-- SIR\. YAON — WHATSAPP -->\s*<div class=\"connect-card whatsapp-partner fade-in\">.*?</a>\s*</div>"
html = re.sub(wa_partner_pattern, "", html, flags=re.DOTALL)

# 6. Add favicon
favicon = "<link rel=\"icon\" href=\"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><circle cx='50' cy='50' r='50' fill='%23111111'/></svg>\">"
html = re.sub(r"(<head>\s*)", rf"\1{favicon}\n    ", html)

with open(r"d:\DOWNLOAD\alchemist4real\index.html", "w", encoding="utf-8") as f:
    f.write(html)
