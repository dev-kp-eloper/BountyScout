```python
bounties = [
    {
        "number": "1.",
        "title": "[LIVE-INTEGRATION r33c5cf9b171f] Invalid generation rejection fixture",
        "repository": "[isearchxsolve/oss-hunter-livefire](https://github.com/isearchxsolve/oss-hunter-livefire)",
        "comments": "0",
        "last_updated": "2026-11-02T17:55:48Z"
    },
    {
        "number": "2.",
        "title": "[LIVE-INTEGRATION r33c5cf9b171f] Correct day-to-second conversion",
        "repository": "[isearchxsolve/oss-hunter-livefire](https://github.com/isearchxsolve/oss-hunter-livefire)",
        "comments": "0",
        "last_updated": "2026-11-02T17:55:21Z"
    },
    {
        "number": "3.",
        "title": "[superteam digest 2026-11-02]",
        "repository": "[airdropia/earn-ops](https://github.com/airdropia/earn-ops)",
        "comments": "0",
        "last_updated": "2026-11-02T17:54:14Z"
    },
    {
        "number": "4.",
        "title": "In a fight at a belt the labels pile up: gang tag under the rock plate, raider readout under BELT B, a raider behind MINING",
        "repository": "[thetazero/retrox](https://github.com/thetazero/retrox)",
        "comments": "0",
        "last_updated": "2026-11-02T17:53:54Z"
    },
    {
        "number": "5.",
        "title": "[Bounty] 💰 Bounty Seguro ($$250): 💰 Bounty Seguro ($$250): [Bounty] 💰 Bounty Seguro",
        "repository": "[zhangjiayang6835-cyber/bounty-plaza](https://github.com/zhangjiayang6835-cyber/bounty-plaza)",
        "comments": "9",
        "last_updated": "2026-11-02T17:53:52Z"
    },
    {
        "number": "6.",
        "title": "A wanted gang can't be fought at its lair: it stalks away, or comes home and never comes out",
        "repository": "[thetazero/retrox](https://github.com/thetazero/retrox)",
        "comments": "0",
        "last_updated": "2026-11-02T17:53:30Z"
    }
]

for bounty in bounties:
    print(f"**{bounty['number']}** {bounty['title']}")
    print(f"- **Repository:** {bounty['repository']}")
    print(f"- **Comments:** {bounty['comments']}")
    print(f"- **Last Updated:** {bounty['last_updated']}\n")
```