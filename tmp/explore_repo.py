import json
import urllib.request
import os

repo = "dev-kp-eloper/BountyScout"
branches = ["main", "master"]
for branch in branches:
    url = f"https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.load(resp)
            print(f"=== Branch: {branch} ===")
            for item in data.get("tree", []):
                print(item["path"])
            break
    except Exception as e:
        print(f"Branch {branch}: {e}")
else:
    print("No main/master branch found")
