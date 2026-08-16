import datetime

class BountyScout:
    def __init__(self, report_title, scan_time):
        self.report_title = report_title
        self.scan_time = scan_time
        self.bounties = []

    def generate_report(self):
        print(f"### Active Bounty Scan Results")
        print(f"**Scan Time:** {self.scan_time}")
        print()
        for idx, item in enumerate(self.bounties, 1):
            print(f#### {idx}. [{item['title']}]")
            print(f"- **Repository:** [{item['repo']}]")
            print(f"- **Comments:** {item['comments']}")
            print(f"- **Last Updated:** {item['last_updated']}")
        print()

bounties = [
    {"title": "[[Security] HIGH: RSA JWK parameter validation missing; MEDIUM: SHA-1 in RSA_OAEP; algorithms=None bypass]", "repo": "mpdavis/python-jose", "comments": "1", "last_updated": "2026-08-16T11:18:05Z"},
    {"title": "[🎯 Bounty Alert: 6 New Opportunityies found]", "repo": "freedom-winds/BountyScout", "comments": "0", "last_updated": "2026-08-16T11:17:57Z"},
    {"title": "[🎯 Bounty Alert: 6 New Opportunityies found]", "repo": "vansh-09/BountyScout", "comments": "0", "last_updated": "2026-08-16T11:17:55Z"},
    {"title": "[[radar] SN open bounty 2026-08-16T11:15]", "repo": "relayhop/ClaudeEarnSelf-runtime", "comments": "0", "last_updated": "2026-08-16T11:15:48Z"},
    {"title": "[Avatar's blanket unoptimized prop defeats Next.js image optimization for every avatar in the app]", "repo": "MergeFi/frontend", "comments": "1", "last_updated": "2026-08-16T11:13:22Z"},
    {"title": "[[radar] SN open bounty 2026-08-16T10:58]", "repo": "relayhop/ClaudeEarnSelf-runtime", "comments": "0", "last_updated": "2026-08-16T10:58:09Z"},
    {"title": "[ZM needs a websocket]", "repo": "ZoneMinder/zoneminder", "comments": "10", "last_updated": "2026-08-16T10:33:18Z"}
]

scout = BountyScout("[$2026.0] 🎯 Bounty Alert: 7 New Opportunityies found", "2026-08-16 11:22 UTC")
scout.bounties = bounties

if __name__ == "__main__":
    scout.generate_report()