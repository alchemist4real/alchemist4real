import urllib.request
import json
import os

req = urllib.request.Request('https://api.github.com/users/alchemist4real/repos?per_page=100&sort=updated', headers={'User-Agent': 'Python'})
try:
    with urllib.request.urlopen(req) as res:
        repos = json.loads(res.read().decode('utf-8'))
        print(f"Total GitHub Repos: {len(repos)}")
        with open("scripts/github_repos.json", "w", encoding="utf-8") as f:
            json.dump(repos, f, indent=2)
except Exception as e:
    print(f"Error fetching GitHub repos: {e}")
