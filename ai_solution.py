```python
def format_github_issues(issues):
    formatted_issues = []
    for issue in issues:
        formatted_issues.append({
            "Repository": issue["Repository"],
            "Issue": f"[{issue['Issue']}]({issue['URL']})",
            "Comments": issue["Comments"],
            "Last Updated": issue["Last Updated"]
        })
    return formatted_issues

# Example usage:
issues = [
    {
        "Repository": "ProSkillsMD/proskills",
        "Issue": "doomsday-proof-of-escrow",
        "URL": "https://github.com/ProSkillsMD/proskills/issues/10003",
        "Comments": "1",
        "Last Updated": "2026-10-25T17:26:08Z"
    },
    # Include other issues similarly
]

formatted_issues = format_github_issues(issues)
for issue in formatted_issues:
    print(issue)
```