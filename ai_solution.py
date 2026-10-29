```python
def format_issues(issues):
    formatted = []
    for issue in issues:
        formatted.append(f"### {issue['number']}. {issue['title']}")
        formatted.append(f"- **Repository:** {issue['repository']}")
        formatted.append(f"- **Comments:** {issue['comments']}")
        formatted.append(f"- **Last Updated:** {issue['last_updated']}")
        formatted.append("---")
    return "\n".join(formatted)

# Example usage:
issues = [
    {
        "number": "1.",
        "title": "[BUG] CLI validator unregister bypasses instruction builder, lacks on-chain lifecycle pre-flight validation, and misses deactivate subcommand",
        "repository": "[paraloom-labs/paraloom-core](https://github.com/paraloom-labs/paraloom-core)",
        "comments": "2",
        "last_updated": "2026-10-28T18:00:39Z"
    },
    # ... other issues
]

print(format_issues(issues))
```