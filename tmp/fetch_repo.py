import json, urllib.request

def fetch(path):
    url = f"https://api.github.com/repos/dev-kp-eloper/BountyScout{path}"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)

# Get repo contents
data = fetch("")
print("Name:", data.get("name"))
print("Default branch:", data.get("default_branch"))
print("Description:", data.get("description"))

# Get root contents
branch = data.get("default_branch", "main")
contents = fetch("/contents")
for item in contents:
    print(f"[{item['type']}] {item['name']}")
