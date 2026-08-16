class BountyScan:
    def __init__(self, name, time):
        self.name = name
        self.time = time
        self.entries = [
            {"n": 1, "title": "TLA - Avatar: The Last Airbender Set Card Implementation Tracking", "repo": "magefree/mage", "comments": 8, "updated": "2026-08-16T14:24:20Z"},
            {"n": 2, "title": "🎯 Bounty Alert: 8 New Opportunityies found", "repo": "vansh-09/BountyScout", "comments": 0, "updated": "2026-08-16T14:20:18Z"},
            {"n": 3, "title": "🎯 Bounty Alert: 6 New Opportunityies found", "repo": "freedom-winds/BountyScout", "comments": 0, "updated": "2026-08-16T14:20:09Z"},
            {"n": 4, "title": "[radar] SN open bounty 2026-08-16T14:18", "repo": "relayhop/ClaudeEarnSelf-runtime", "comments": 1, "updated": "2026-08-16T14:18:24Z"},
            {"n": 5, "title": "TeamsService, MaintenancePoolService, and UsersService have zero test coverage despite directly controlling money movement and payout-address changes", "repo": "MergeFi/backend", "comments": 1, "updated": "2026-08-16T14:13:20Z"},
            {"n": 6, "title": "[radar] SN open bounty 2026-08-16T13:58", "repo": "relayhop/ClaudeEarnSelf-runtime", "comments": 1, "updated": "2026-08-16T14:10:41Z"},
            {"n": 7, "title": "[radar] SN open bounty 2026-08-16T14:00", "repo": "relayhop/sn-monetization-runtime", "comments": 0, "updated": "2026-08-16T14:00:17Z"},
            {"n": 8, "title": "[Bug]: Spawn on first join", "repo": "BeestoXd/UltimateDonutSMP", "comments": 0, "updated": "2026-08-16T14:00:17Z"},
        ]

    def __str__(self):
        output = f"Title: [{self.name}]\n"
        output += "Details: ### Active Bounty Scan Results\n\n"
        output += f"**Scan Time:** {self.time}\n\n"
        for entry in self.entries:
            output += f"#### {entry['n']}. [{entry['title']}]\n"
            output += f"- **Repository:** [{entry['repo']}]\n"
            output += f"- **Comments:** {entry['comments']}\n"
            output += f"- **Last Updated:** {entry['updated']}\n"
        return output

if __name__ == "__main__":
    report = BountyScan("[$2026.0] 🎯 Bounty Alert: 8 New Opportunityies found", "2026-08-16 14:25 UTC")
    print(report)