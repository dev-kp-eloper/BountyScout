```python
def get_latest_bounties(bounties):
    return [
        {
            "id": f"{i+1}. {bounty['id']}",
            "title": bounty["title"],
            "repository": bounty["repository"],
            "comments": str(bounty["comments"]),
            "last_updated": bounty["last_updated"]
        }
        for i, bounty in enumerate(bounties)
    ]
```