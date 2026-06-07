import os
import sys
import shutil

import subprocess

def main():
    print("Running AI Research Sync...")
    
    script_path = os.path.join("scripts", "sync-research.py")
    result = subprocess.run([sys.executable, script_path])
    if result.returncode != 0:
        print("sync-research.py failed!")
        sys.exit(result.returncode)

    print("Copying files to dist...")
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)

    # Files and folders to serve statically
    targets = [
        "index.html",
        "dashboard.html",
        "viewer.html",
        "data.json",
        "heartbeat.json",
        "assets",
        "research"
    ]

    for t in targets:
        if os.path.exists(t):
            dest = os.path.join(dist_dir, t)
            if os.path.isdir(t):
                print(f"Copying directory {t} to {dest}")
                shutil.copytree(t, dest)
            else:
                print(f"Copying file {t} to {dest}")
                shutil.copy2(t, dest)
        else:
            print(f"Warning: target {t} does not exist.")

    print("Build complete.")

if __name__ == "__main__":
    main()
